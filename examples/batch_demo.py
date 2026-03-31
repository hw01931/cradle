import time
import random
import logging
import sys
from cradle import cradle_watch

# 로깅 설정
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger("DataPipeline")

# 데이터 파이프라인 시뮬레이션
@cradle_watch(project="nightly-data-pipeline")
def run_data_pipeline():
    logger.info("Starting processing 10TB of data...")
    time.sleep(1)
    
    # 일부러 에러 발생
    simulate_memory_corruption()

def simulate_memory_corruption():
    logger.info("Transforming datasets...")
    time.sleep(1)
    raise MemoryError("Data transformation failed. Out of memory during join operation.")

if __name__ == "__main__":
    logger.info("Initializing Nightly Batch Job")
    
    # 별도의 웹 서버(FastAPI) 없이도 에러를 감지하고 
    # Cradle SRE 루프(진단 -> 리포팅 -> 조치 제안)가 실행됩니다!
    try:
        run_data_pipeline()
    except Exception as e:
        logger.error("Pipeline crashed, but Cradle has already reported it.")
