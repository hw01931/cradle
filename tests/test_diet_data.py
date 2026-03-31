import pytest
from cradle.diet import get_diet_data

def test_get_diet_data_pynvml_stats():
    # Test PII masking and long string truncation
    sensitive_data = {"api_key": "mysecretkey", "user_id": 12345, "content": "A" * 200}
    diet_data = get_diet_data(sensitive_data)
    
    assert diet_data["api_key"] == "********"
    assert diet_data["user_id"] == 12345
    assert "..." in diet_data["content"]
    assert len(diet_data["content"]) < 200
