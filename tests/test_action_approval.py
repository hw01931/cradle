import pytest
from cradle.action import ActionManager

@pytest.fixture
def manager():
    return ActionManager()

@pytest.mark.asyncio
async def test_require_approval_workflow(manager):
    # 'restart' requires approval in default config
    result = await manager.execute("restart")
    assert result["status"] == "pending_approval"
    assert "action_id" in result
    
    action_id = result["action_id"]
    # Verify it is in the pending list
    assert action_id in manager.pending_actions
    
    # Approve it
    approval_result = await manager.approve(action_id)
    assert approval_result["status"] == "success"
    assert action_id not in manager.pending_actions
