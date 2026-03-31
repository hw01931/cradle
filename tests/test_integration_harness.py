import pytest
import json
from cradle.diet import get_diet_traceback
from cradle.data import data_manager

@pytest.mark.asyncio
async def test_integrated_report_generation():
    # Simulate an error
    try:
        1 / 0
    except ZeroDivisionError as e:
        traceback_json = get_diet_traceback(e)
        db_context = await data_manager.fetch_error_context()
        
        # Verify the structure
        assert "ZeroDivisionError" in traceback_json
        assert "db_stats" in db_context
        assert db_context["db_stats"]["status"] == "connected"
