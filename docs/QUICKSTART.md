# Quick Start Guide ⚡

Follow these steps to integrate Project Cradle into your existing backend in 5 minutes.

## 📦 Installation

```bash
pip install cradle
```

## 🛠️ Configuration

Create a `cradle.yml` file in your project's root directory.

```yaml
# cradle.yml
project: "my-production-service"
model: "gpt-4-turbo" # The LLM model to use
action:
  # Sensitive actions require explicit human approval
  require_approval: ["restart", "scale_up", "cleanup_logs"]
  auto_recover: true
metrics:
  # Trigger diagnosis if CPU usage exceeds 80%
  cpu_threshold: 80.0
```

## 🔌 Integration (FastAPI)

```python
from fastapi import FastAPI
from cradle import CradleMiddleware

app = FastAPI()

# Add this line to activate Cradle! 🌌
app.add_middleware(CradleMiddleware)

@app.get("/")
def home():
    return {"msg": "Autonomous Reliability is enabled."}
```

## 🕵️‍♂️ Monitoring & Approval

Cradle will automatically analyze failures or high resource usage. If an action requiring approval is proposed, approve it as follows:

```bash
# Check the status of your foundation
cradle status

# Approve the action using the action_id from the report
cradle approve 8a2b1c
```

## 🛡️ True 24/7 Autonomous Monitoring

Project Cradle includes a **Background Sentinel** that runs independently of incoming web traffic. Even if your service has zero visitors at 3 AM, Cradle will wake up every `metrics.interval` (default: 60s) to check system health.

- **Proactive Background Checks**: Detects resource leaks or high CPU before users notice.
- **Silent Recovery**: If `auto_recover` is enabled, Cradle will perform the fix silently while you sleep.

Your server is now ready to autonomously monitor, report, and recover! 🚀
