import pytest
import os
import json
from src.cradle.diet import get_diet_traceback

def test_diet_traceback_filtering():
    """
    트레이스백에서 'site-packages' 등 외부 경로가 필터링되는지 확인합니다.
    """
    try:
        # 강제로 에러 발생
        raise ValueError("Test Error")
    except Exception as e:
        diet_json = get_diet_traceback(e)
        diet_data = json.loads(diet_json)

    assert diet_data["type"] == "ValueError"
    assert diet_data["msg"] == "Test Error"
    
    # 스택 프레임 중 하나라도 본 테스트 파일이어야 함
    has_this_file = False
    for frame in diet_data["stack"]:
        # 외부 경로는 없어야 함
        assert "site-packages" not in frame["f"]
        if "test_diet.py" in frame["f"]:
            has_this_file = True
            
    assert has_this_file

def test_diet_max_stack_depth():
    """
    트레이스백 프레임 수가 제한되는지 확인합니다.
    """
    def deep_recursion(n):
        if n == 0:
            raise RuntimeError("Deep Error")
        deep_recursion(n - 1)

    try:
        deep_recursion(20)
    except Exception as e:
        # 5개로 제한
        diet_json = get_diet_traceback(e, max_stack_depth=5)
        diet_data = json.loads(diet_json)

    assert len(diet_data["stack"]) == 5
