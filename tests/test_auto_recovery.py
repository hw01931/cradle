import pytest
import json
from cradle.core import cradle_agent
from cradle.action import action_manager

@pytest.mark.asyncio
async def test_auto_recovery_execution():
    # Simulate a trigger that LLM will recommend 'restart'
    report_data = {
        "error": {"type": "ValueError"},
        "trigger": "EXCEPTION"
    }
    
    # We test the loop logic
    await cradle_agent.complete_sre_loop(ValueError("Test"), report_data)
    
    # Check if 'action_result' is present in report_data (modified by the loop)
    assert "action_result" in report_data
    assert report_data["action_result"]["status"] in ["success", "pending_approval", "dry_run"]
