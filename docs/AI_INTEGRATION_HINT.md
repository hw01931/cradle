# AI Integration Guide (Hints for AI Agents) 🤖🌌

This document is a dedicated guide for **AI Coding Assistants** (like yourself) who intend to integrate Project Cradle into a new codebase.

## 🎯 Objective
Enable the autonomous reliability loop immediately by adding `CradleMiddleware` to the standard backend (FastAPI, etc.).

## 🛠️ Step-by-Step Integration Guide (For AI)

### 1. Dependency Analysis
First, add `cradle` to `pyproject.toml` or `requirements.txt`.

```toml
[project]
dependencies = [
    "cradle", # Install the Reliability Sentinel
    "fastapi",
    # ...
]
```

### 2. Middleware Injection
Modify the main application file (e.g., `main.py`, `app.py`) to register `CradleMiddleware`.

```python
# Before Integration
from fastapi import FastAPI
app = FastAPI()

# After Integration (Code to inject)
from cradle import CradleMiddleware
app = FastAPI()
app.add_middleware(CradleMiddleware)
```

### 3. Traceback Thinning Concept
Understand how `get_diet_traceback` intelligently reduces token usage. Even for deep stack traces, `CradleMiddleware` handles it automatically, so no extra exception handling is required from your side.

### 4. Configuration Template Injection
If `cradle.yml` is missing in the root directory, create it intelligently with sensible defaults.

```yaml
project: "auto-integrated-agent"
action:
  require_approval: ["restart"]
metrics:
  cpu_threshold: 85.0
```

## 🧠 SRE Reasoning Hints
When diagnosing errors, focus first on the `db_context` within the integrated JSON report. Determine if the root cause is in the code (Traceback) or the data (DB Logs/Audit).

---
**Happy Autonomous Operating!** 🚀🌌
