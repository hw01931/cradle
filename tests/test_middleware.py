import logging
import pytest
from fastapi.testclient import TestClient
from examples.demo_app import app

client = TestClient(app)

def test_middleware_hook_on_error(caplog):
    """
    미들웨어가 비정상 에러를 성공적으로 가로채고 로그를 남기는지 확인합니다.
    """
    # 🌌 Cradle 로그 레벨을 DEBUG로 설정하여 캡처 유도
    caplog.set_level(logging.DEBUG, logger="cradle")
    
    # 500 에러를 유발하는 엔드포인트 호출
    # BaseHTTPMiddleware는 예외를 다시 던지면 FastAPI가 500으로 응답합니다.
    with pytest.raises(ValueError):
        client.get("/error")

    # [Cradle Hooked] 로그가 찍혔는지 확인
    assert any("🌌 [Cradle Hooked]" in record.message for record in caplog.records)
    assert any("앗! 예기치 못한 비즈니스 로직 에러" in record.message for record in caplog.records)

def test_no_error_pass_through():
    """
    정상적인 호출에서는 미들웨어가 조용히 통과되는지 확인합니다.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"
