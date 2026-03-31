# Project Cradle: The Universal Foundation for Autonomous Reliability 🌌🛡️

Project Cradle is the **Unified Foundation** that orchestrates specialized reliability harnesses to ensure your software never stops. It acts as the "Cradle"—a secure, intelligent container that holds your code, data, and actions together.

## 🏗️ The Metaphor
Cradle is not just an agent; it is the **infrastructure for autonomy**. It provides the core intelligence and lifecycle management for four specialized **Harnesses**:
1. **Code Harness**: Deep visibility and diagnostic hooks into your logic.
2. **Data Harness**: Secure, automated context retrieval and PII-masked logging.
3. **Action Harness**: The hands of the system—executing recovery and scaling.
4. **Metric Harness (The Sentinel)**: The eyes that watch for anomalies before they become failures.

## 🚀 Key Features

- **Autonomous Orchestration**: Cradle coordinates all harnesses to perform seamless diagnosis and recovery under human oversight.
- **Universal Watcher**: Use `@cradle_watch` to protect anything—from FastAPI endpoints to 10TB data pipelines.
- **GitOps-First**: Every incident generates a detailed report, a fix branch, and a Pull Request automatically.
- **Human-in-the-Loop**: Cradle proposes actions, but you stay in control with mandatory approval for sensitive operations.

## 📦 Installation

```bash
# Install in local development mode
pip install -e .

# Or (When published to PyPI)
pip install cradle-sre
```

## ⚡ Quick Start (FastAPI Example)

```python
from fastapi import FastAPI
from cradle import CradleMiddleware

app = FastAPI()

# Just add this middleware to start autonomous operations!
app.add_middleware(CradleMiddleware)

@app.get("/")
def home():
    return {"msg": "Cradle is watching over this server."}
```

## 📖 Documentation

- [Quick Start Guide](docs/QUICKSTART.md)
- [Configuration Reference](docs/CONFIGURATION.md)
- [AI Integration Guide (For AI Agents)](docs/AI_INTEGRATION_HINT.md)

---
Achieve 24/7 zero-downtime service with Project Cradle. 🚀
