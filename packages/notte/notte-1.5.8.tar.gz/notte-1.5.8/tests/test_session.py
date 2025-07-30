from collections import Counter

import notte_core
import pytest
from notte_browser.captcha import CaptchaHandler
from notte_browser.errors import CaptchaSolverNotAvailableError, NoSnapshotObservedError
from notte_browser.session import NotteSession, SessionTrajectoryStep
from notte_core.actions import (
    ClickAction,
    GotoAction,
    InteractionAction,
    ScrollDownAction,
    WaitAction,
)
from notte_core.browser.snapshot import BrowserSnapshot
from notte_core.llms.service import LLMService
from pydantic import ValidationError

from tests.mock.mock_browser import MockBrowserDriver
from tests.mock.mock_service import MockLLMService
from tests.mock.mock_service import patch_llm_service as _patch_llm_service

patch_llm_service = _patch_llm_service

notte_core.set_error_mode("developer")


@pytest.fixture
def mock_llm_response() -> str:
    return """
| ID  | Description | Parameters | Category |
| L1  | Opens more information page | | Navigation |
"""


@pytest.fixture
def mock_llm_service(mock_llm_response: str) -> MockLLMService:
    return MockLLMService(
        mock_response=f"""
<document-summary>
This is a mock document summary
</document-summary>
<document-category>
homepage
</document-category>
<action-listing>
{mock_llm_response}
</action-listing>
"""
    )


@pytest.mark.asyncio
async def test_context_property_before_observation(patch_llm_service: MockLLMService) -> None:
    """Test that accessing context before observation raises an error"""
    with pytest.raises(
        NoSnapshotObservedError,
    ):
        async with NotteSession(window=MockBrowserDriver()) as page:
            _ = page.snapshot


@pytest.mark.asyncio
async def test_context_property_after_observation(patch_llm_service: MockLLMService) -> None:
    """Test that context is properly set after observation"""
    async with NotteSession(window=MockBrowserDriver()) as page:
        _ = await page.aobserve("https://notte.cc")

    # Verify context exists and has expected properties
    assert isinstance(page.snapshot, BrowserSnapshot)
    assert page.snapshot.metadata.url == "https://notte.cc"
    assert page.snapshot.a11y_tree is None
    assert page.snapshot.dom_node is not None


@pytest.mark.asyncio
async def test_trajectory_empty_before_observation(patch_llm_service: MockLLMService) -> None:
    """Test that list_actions returns None before any observation"""
    async with NotteSession(window=MockBrowserDriver()) as page:
        assert len(page.trajectory) == 0


@pytest.mark.asyncio
async def test_valid_observation_after_observation(patch_llm_service: MockLLMService) -> None:
    """Test that last observation returns valid actions after observation"""
    async with NotteSession(window=MockBrowserDriver()) as page:
        obs = await page.aobserve("https://example.com")

    assert obs.space is not None
    actions = obs.space.interaction_actions
    assert isinstance(actions, list)
    assert all(isinstance(action, InteractionAction) for action in actions)
    assert len(actions) == 1  # Number of actions in mock response

    # Verify each action has required attributes
    actions = [
        ClickAction(id="L1", description="Opens more information page", category="Navigation"),
    ]


@pytest.mark.skip(reason="TODO: fix this")
@pytest.mark.asyncio
async def test_valid_observation_after_step(patch_llm_service: MockLLMService) -> None:
    """Test that last observation returns valid actions after taking a step"""
    # Initial observation
    async with NotteSession(window=MockBrowserDriver()) as page:
        obs = await page.aobserve("https://example.com")
        initial_actions = obs.space.interaction_actions
        assert initial_actions is not None
        assert len(initial_actions) == 1

        # Take a step
        _ = await page.astep(type="click", action_id="L1")  # Using L1 from mock response

        # TODO: verify that the action space is updated


@pytest.mark.asyncio
async def test_valid_observation_after_reset(patch_llm_service: MockLLMService) -> None:
    """Test that last observation returns valid actions after reset"""
    # Initial observation
    async with NotteSession(window=MockBrowserDriver()) as page:
        obs = await page.aobserve("https://example.com")

        # Reset environment
        await page.areset()
        obs = await page.aobserve("https://example.com")

        # Verify new observation is correct
        assert len(obs.space.interaction_actions) > 0
        assert "https://example.com" in obs.metadata.url

        # Verify the state was effectively reset
        assert page.snapshot.screenshot == obs.screenshot.raw  # poor proxy but ok
        assert len(page.trajectory) == 1  # the trajectory should only contains a single obs (from reset)


@pytest.mark.asyncio
async def test_llm_service_from_config(patch_llm_service: MockLLMService, mock_llm_response) -> None:
    """Test that LLMService.from_config returns the mock service"""
    service = LLMService.from_config()
    assert isinstance(service, MockLLMService)
    assert service.mock_response == patch_llm_service.mock_response
    assert mock_llm_response in (await service.completion(prompt_id="test", variables={})).choices[0].message.content


@pytest.mark.asyncio
async def test_callback_should_be_called_once_per_observation(patch_llm_service: MockLLMService) -> None:
    """Test that the callback is called once per observation"""
    counter = Counter(callback_count=0)

    def callback(step: SessionTrajectoryStep) -> None:
        counter["callback_count"] += 1

    async with NotteSession(enable_perception=False, act_callback=callback) as page:
        obs = await page.astep(action=GotoAction(url="https://example.com"))
        obs = await page.aobserve()
        assert obs.space is not None
        assert len(obs.space.interaction_actions) == 1
        assert len(page.trajectory) == 1
        assert counter["callback_count"] == 1


@pytest.mark.asyncio
async def test_step_should_fail_without_observation() -> None:
    """Test that step should fail without observation"""
    async with NotteSession(enable_perception=False) as page:
        with pytest.raises(NoSnapshotObservedError):
            _ = await page.astep(action=ClickAction(id="L1"))


@pytest.mark.asyncio
async def test_step_should_succeed_after_observation() -> None:
    """Test that step should fail without observation"""
    async with NotteSession(enable_perception=False) as page:
        _ = await page.aobserve(url="https://example.com")
        _ = await page.astep(action=ClickAction(id="L1"))


@pytest.mark.asyncio
async def test_browser_action_step_should_succeed_without_observation() -> None:
    """Test that step should fail without observation"""
    async with NotteSession(enable_perception=False) as page:
        _ = await page.astep(action=GotoAction(url="https://example.com"))
        _ = await page.astep(action=ScrollDownAction())
        _ = await page.astep(action=WaitAction(time_ms=1000))


@pytest.mark.asyncio
@pytest.mark.parametrize("action_id", ["INVALID_ACTION_ID", "B999", "X999"])
async def test_step_with_invalid_action_id_returns_failed_result(action_id: str):
    """Test that stepping with an invalid action ID returns a failed StepResult."""

    async with NotteSession(enable_perception=False) as session:
        # First observe a page to get a snapshot
        _ = await session.aobserve(url="https://example.com")
        # Try to step with an invalid action ID that doesn't exist on the page
        step_response = await session.astep(type="click", action_id=action_id)

        # Verify that the step failed
        assert not step_response.success
        assert "invalid" in step_response.message.lower() or "not found" in step_response.message.lower()
        assert step_response.exception is not None


@pytest.mark.asyncio
async def test_step_with_empty_action_id_should_fail_validation_pydantic():
    """Test that stepping with an invalid action ID returns a failed StepResult."""

    async with NotteSession(enable_perception=False) as session:
        # First observe a page to get a snapshot
        _ = await session.aobserve(url="https://example.com")
        # Try to step with an invalid action ID that doesn't exist on the page
        with pytest.raises(ValidationError):
            _ = await session.astep(type="click", action_id="")


def test_captcha_solver_not_available_error():
    with pytest.raises(CaptchaSolverNotAvailableError):
        _ = NotteSession(enable_perception=False, solve_captchas=True)

    CaptchaHandler.is_available = True
    _ = NotteSession(enable_perception=False, solve_captchas=True)
    CaptchaHandler.is_available = False
