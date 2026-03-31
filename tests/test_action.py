import pytest
from cradle.action import ActionManager

@pytest.fixture
def action_manager():
    return ActionManager()

@pytest.mark.asyncio
async def test_execute_restart(action_manager):
    result = await action_manager.execute("restart")
    assert result["status"] == "pending_approval"
    assert "approval" in result["msg"].lower()

@pytest.mark.asyncio
async def test_execute_invalid_action(action_manager):
    result = await action_manager.execute("invalid")
    assert result["status"] == "denied"
    assert "not in allowed_actions" in result["reason"].lower()
