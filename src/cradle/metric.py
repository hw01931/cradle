import logging
import psutil
from typing import Dict, Any, Optional
from cradle.config import config

logger = logging.getLogger("cradle.metric")

class MetricManager:
    def __init__(self):
        self.cpu_threshold = config.get("metrics.cpu_threshold", 80.0)
        self.mem_threshold = config.get("metrics.mem_threshold", 80.0)
        self.vram_threshold = config.get("metrics.vram_threshold", 85.0)
        self.has_gpu = False
        
        try:
            import pynvml
            pynvml.nvmlInit()
            self.has_gpu = True
            self.device_count = pynvml.nvmlDeviceGetCount()
            logger.info(f"📊 [MetricManager] GPU Monitoring Enabled. Found {self.device_count} GPUs.")
        except Exception:
            logger.info("📊 [MetricManager] No GPU available or pynvml missing. Running in CPU-only mode.")
            
        logger.info(f"📊 [MetricManager] Limits Configured (CPU={self.cpu_threshold}%, MEM={self.mem_threshold}%, VRAM={self.vram_threshold}%)")

    def get_current_metrics(self) -> Dict[str, Any]:
        """
        현재 시스템 리소스 지표를 수집합니다. GPU가 있으면 VRAM 상태도 수집합니다.
        """
        metrics = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "boot_time": psutil.boot_time(),
        }
        
        if self.has_gpu:
            import pynvml
            gpu_stats = []
            max_vram_percent = 0.0
            
            for i in range(self.device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                vram_pct = (mem_info.used / mem_info.total) * 100
                gpu_stats.append({
                    "id": i,
                    "vram_percent": round(vram_pct, 1),
                    "used_mb": mem_info.used // (1024*1024),
                    "total_mb": mem_info.total // (1024*1024)
                })
                max_vram_percent = max(max_vram_percent, vram_pct)
                
            metrics["gpu_metrics"] = gpu_stats
            metrics["max_vram_percent"] = round(max_vram_percent, 1)

        return metrics

    def check_anomaly(self) -> Optional[Dict[str, Any]]:
        """
        임계치를 초과하는 이상 징후가 있는지 확인합니다.
        """
        metrics = self.get_current_metrics()
        
        anomalies = {}
        if metrics["cpu_percent"] > self.cpu_threshold:
            anomalies["cpu"] = f"High CPU usage: {metrics['cpu_percent']}%"
        
        if metrics["memory_percent"] > self.mem_threshold:
            anomalies["memory"] = f"High Memory usage: {metrics['memory_percent']}%"
            
        if self.has_gpu and metrics.get("max_vram_percent", 0) > self.vram_threshold:
            anomalies["gpu_vram"] = f"Critical GPU VRAM usage: {metrics['max_vram_percent']}%"

        if anomalies:
            logger.warning(f"🚨 [MetricManager] Anomaly detected: {anomalies}")
            return {
                "type": "METRIC_ANOMALY",
                "details": anomalies,
                "metrics": metrics
            }
        
        return None

# Global instance
metric_manager = MetricManager()
