import pytest
from cradle.metric import MetricManager

@pytest.fixture
def metric_manager():
    return MetricManager()

def test_get_current_metrics(metric_manager):
    metrics = metric_manager.get_current_metrics()
    assert "cpu_percent" in metrics
    assert "memory_percent" in metrics
    assert "disk_percent" in metrics

def test_check_anomaly_none(metric_manager):
    # Default threshold is 80%, unless someone is hogging the CPU, it should be None
    anomaly = metric_manager.check_anomaly()
    if anomaly:
        assert anomaly["type"] == "METRIC_ANOMALY"
    else:
        assert anomaly is None
