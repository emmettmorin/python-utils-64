import os
import json
from typing import Any, Dict, Optional

DEFAULT_ROBLOX_CONFIG: Dict[str, Any] = {
    "cookie": "",
    "place_id": 0,
    "universe_id": 0,
    "request_timeout": 15.0,
    "max_retries": 3,
    "proxy_url": None,
    "user_agent": "Roblox/WinInet",
    "rate_limit_delay": 0.5,
}

class RobloxConfig(dict):
    """Configuration container for Roblox API tools with recursive fallbacks."""

    def __init__(self, filepath: Optional[str] = None, **overrides: Any) -> None:
        super().__init__(**DEFAULT_ROBLOX_CONFIG)
        if filepath and os.path.exists(filepath):
            self._load_from_file(filepath)
        self.update({k: v for k, v in overrides.items() if v is not None})
        self._sync_env_vars()

    def _load_from_file(self, filepath: str) -> None:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self.update(data)
        except (json.JSONDecodeError, OSError):
            pass

    def _sync_env_vars(self) -> None:
        for key in list(self.keys()):
            env_key = f"ROBLOX_{key.upper()}"
            if env_key in os.environ:
                val = os.environ[env_key]
                target_type = type(self[key])
                if target_type is bool:
                    self[key] = val.lower() in ("1", "true", "yes")
                elif target_type in (int, float):
                    try:
                        self[key] = target_type(val)
                    except ValueError:
                        pass
                else:
                    self[key] = val

    def __getattr__(self, item: str) -> Any:
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"'RobloxConfig' object has no attribute '{item}'")

    def __setattr__(self, key: str, value: Any) -> None:
        self[key] = value

    def export(self, filepath: str) -> bool:
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(dict(self), f, indent=4)
            return True
        except OSError:
            return False
