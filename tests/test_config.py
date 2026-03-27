import os
import pytest
import yaml
from src.cradle.config import CradleConfig

@pytest.fixture
def mock_config_file(tmp_path):
    config_data = {
        "project": "test-cradle",
        "api_key": "${TEST_API_KEY}",
        "diet": {
            "max_stack_depth": 5
        }
    }
    config_file = tmp_path / "cradle.yml"
    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config_data, f)
    return str(config_file)

def test_config_loading_and_env_substitution(mock_config_file, monkeypatch):
    """
    cradle.yml 파일을 로드하고 환경 변수 치환이 정상적으로 수행되는지 확인합니다.
    """
    # 환경 변수 설정
    monkeypatch.setenv("TEST_API_KEY", "sk-test-12345")
    
    # 설정 로드
    conf = CradleConfig(config_file=mock_config_file)
    
    assert conf.get("project") == "test-cradle"
    assert conf.get("api_key") == "sk-test-12345"
    assert conf.get("diet.max_stack_depth") == 5
    # Default values checked
    assert conf.get("provider") == "openai"

def test_config_defaults_when_no_file():
    """
    설정 파일이 없을 때 기본값이 정상적으로 로드되는지 확인합니다.
    """
    conf = CradleConfig(config_file="non_existent.yml")
    assert conf.get("project") == "cradle-project"
    assert conf.get("diet.max_stack_depth") == 10
