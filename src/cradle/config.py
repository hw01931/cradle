import os
import re
import yaml
from typing import Any, Dict, Optional

class CradleConfig:
    def __init__(self, config_file: str = "cradle.yml"):
        self.config_path = config_file
        self.data: Dict[str, Any] = self._load_defaults()
        
        if os.path.exists(self.config_path):
            self._load_from_file()

    def _load_defaults(self) -> Dict[str, Any]:
        return {
            "project": "cradle-project",
            "provider": "openai",
            "model": "gpt-4-turbo",
            "api_key": None,
            "diet": {
                "max_stack_depth": 10,
            },
            "git": {
                "auto_pr": True,
                "branch_prefix": "cradle-fix/",
            }
        }

    def _load_from_file(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            file_data = yaml.safe_load(f)
            if file_data:
                self._update_recursive(self.data, file_data)
        
        # Env var substitution
        self.data = self._substitute_env_vars(self.data)

    def _update_recursive(self, base_dict: Dict, update_dict: Dict):
        for k, v in update_dict.items():
            if isinstance(v, dict) and k in base_dict and isinstance(base_dict[k], dict):
                self._update_recursive(base_dict[k], v)
            else:
                base_dict[k] = v

    def _substitute_env_vars(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: self._substitute_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._substitute_env_vars(v) for v in data]
        elif isinstance(data, str):
            # Regex to find ${VAR_NAME} or $VAR_NAME
            pattern = re.compile(r"\$\{?([A-Z0-9_]+)\}?")
            def replace(match):
                var_name = match.group(1)
                return os.environ.get(var_name, match.group(0))
            return pattern.sub(replace, data)
        return data

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        val = self.data
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return default

# Global instance for easy access
config = CradleConfig()
