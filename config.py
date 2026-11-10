import json
import os
from typing import Any, Dict, Optional


class RobloxConfig:
    """Dynamic Roblox API configuration manager with sensible defaults."""

    DEFAULT_CONFIG: Dict[str, Any] = {
        "universe_id": 0,
        "place_id": 0,
        "api_key": "",
        "cookie": "",
        "cloud_base_url": "https://apis.roblox.com/",
        "max_retries": 3,
        "backoff_factor": 1.5,
        "timeout": 30.0,
        "user_agent": "PythonUtils64-RobloxClient/1.0",
        "proxy_url": None,
    }

    def __init__(self, custom_config: Optional[Dict[str, Any]] = None):
        self._storage: Dict[str, Any] = dict(self.DEFAULT_CONFIG)
        if custom_config:
            self._storage.update(custom_config)
        self._apply_env_overrides()

    def _apply_env_overrides(self) -> None:
        """Override configuration values with ROBLOX_* environment variables."""
        for key in self.DEFAULT_CONFIG:
            env_key = f"ROBLOX_{key.upper()}"
            if env_key in os.environ:
                val = os.environ[env_key]
                default_type = type(self.DEFAULT_CONFIG[key])
                if default_type is bool:
                    self._storage[key] = val.lower() in ("1", "true", "yes")
                elif default_type in (int, float) and default_type is not type(None):
                    try:
                        self._storage[key] = default_type(val)
                    except ValueError:
                        pass
                else:
                    self._storage[key] = val

    def load_file(self, filepath: str) -> None:
        """Load configuration settings from a JSON file."""
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self._storage.update(data)
                    self._apply_env_overrides()

    def __getattr__(self, name: str) -> Any:
        if name in self._storage:
            return self._storage[name]
        raise AttributeError(f"Configuration key '{name}' does not exist.")

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def export(self) -> Dict[str, Any]:
        """Return sanitized active configuration copy."""
        redacted = dict(self._storage)
        if redacted.get("cookie"):
            redacted["cookie"] = redacted["cookie"][:10] + "..."
        if redacted.get("api_key"):
            redacted["api_key"] = redacted["api_key"][:4] + "..."
        return redacted
