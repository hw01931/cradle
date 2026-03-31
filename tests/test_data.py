import pytest
from cradle.data import DataManager

@pytest.fixture
def data_manager():
    return DataManager()

@pytest.mark.asyncio
async def test_fetch_error_context(data_manager):
    context = await data_manager.fetch_error_context()
    assert "db_stats" in context
    assert context["db_stats"]["status"] == "connected"
    assert "recent_logs" in context
    assert len(context["recent_logs"]) > 0
