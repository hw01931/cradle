# Configuration Reference ⚙️

Project Cradle uses the `cradle.yml` file to manage all agent behaviors.

## 📝 `cradle.yml` Key Options

| Key | Description | Default |
| --- | --- | --- |
| `project` | Project name for report identification | `cradle-project` |
| `provider` | LLM provider (`openai`, `anthropic`, `google`) | `openai` |
| `model` | Specific LLM model to use | `gpt-4-turbo` |
| `db.url` | DB URI to read audit logs from | `sqlite+aiosqlite:///./cradle.db` |
| `action.allowed_actions` | List of executable actions | `["restart", "scale_up", "cleanup_logs"]` |
| `action.require_approval` | Actions requiring human approval | `["restart", "scale_up"]` |
| `metrics.cpu_threshold` | CPU threshold to trigger proactive reliability (%) | `80.0` |
| `alerts.slack_webhook` | Webhook URL for Slack alerts | `None` |
| `git.auto_pr` | Whether to create Git branches for reports | `True` |

---

## 🤖 Multi-Model Setup

Cradle supports multiple LLM providers. Simply set the `provider` and `api_key`.

```yaml
# For Anthropic Claude
provider: "anthropic"
api_key: "sk-ant-..."
model: "claude-3-sonnet-20240229"
```

---

## 🔒 Security & Data Diet (PII Masking)

Cradle includes a sophisticated **Data Diet Engine** to prevent PII leaks. Add custom keys via the `CRADLE_MASK_KEYS` environment variable.

### Default Masked Keywords
- `password`, `secret`, `token`, `key`, `auth`, `api_key`

---

## 🛡️ Proactive Sentinel Settings

Monitor your server health more aggressively:

```yaml
metrics:
  cpu_threshold: 60.0 # Warning starts at 60%
  mem_threshold: 70.0
  interval: 30 # Check every 30 seconds
```

## 🚨 Alerting Integration

Receive emergency alerts on Slack or Discord:

```yaml
alerts:
  slack_webhook: "https://hooks.slack.com/services/..."
```

Tweak these settings to optimize the agent for your production environment! 🌌🛡️
