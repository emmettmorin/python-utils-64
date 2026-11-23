import json
import os
from typing import Any, Dict, Optional

DEFAULT_ROBLOX_CONFIG: Dict[str, Any] = {
    "universe_id": 0,
    "place_id": 0,
    "open_cloud_api_key": "",
    "roblosecurity": "",
    "base_url": "https://apis.roblox.com",
    "request_timeout": 30.0,
    "max_retries": 3,
    "telemetry_enabled": True,
    "data_store_scope": "global",
}


class DynamicRobloxConfig:
    """Roblox configuration manager with layered defaults and env overrides."""

    def __init__(
        self, filepath: Optional[str] = None, overrides: Optional[Dict[str, Any]] = None
    ):
        self._storage: Dict[str, Any] = dict(DEFAULT_ROBLOX_CONFIG)
        if filepath and os.path.exists(filepath):
            self._load_file(filepath)
        if overrides:
            self._storage.update(overrides)
        self._apply_env_vars()

    def _load_file(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                self._storage.update(data)

    def _apply_env_vars(self) -> None:
        for key, default_val in DEFAULT_ROBLOX_CONFIG.items():
            env_key = f"ROBLOX_{key.upper()}"
            if env_key in os.environ:
                val = os.environ[env_key]
                target_type = type(default_val)
                if target_type is bool:
                    self._storage[key] = val.lower() in ("true", "1", "yes")
                elif target_type in (int, float):
                    self._storage[key] = target_type(val)
                else:
                    self._storage[key] = val

    def __getattr__(self, name: str) -> Any:
        if name in self._storage:
            return self._storage[name]
        raise AttributeError(f"Invalid Roblox config key: '{name}'")

    def __getitem__(self, item: str) -> Any:
        return self.__getattr__(item)

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._storage)
