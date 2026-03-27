import logging
import sys
from fastapi import FastAPI
from src.cradle import CradleMiddleware

# Configure logging to see Cradle's output
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(title="Project Cradle Demo App")

# Hooking the Cradle!
app.add_middleware(CradleMiddleware)

@app.get("/")
def read_root():
    return {"status": "running", "msg": "Cradle is watching..."}

@app.get("/error")
def trigger_error():
    raise ValueError("앗! 예기치 못한 비즈니스 로직 에러가 발생했습니다.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
