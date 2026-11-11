import json
import os
from typing import Any, Dict, Optional


class RobloxConfig:
    """Dynamic configuration loader for Roblox Open Cloud and place APIs."""

    _DEFAULTS: Dict[str, Any] = {
        "universe_id": 0,
        "place_id": 0,
        "api_key": "",
        "cookie": "",
        "datastore_name": "GlobalDataStore",
        "scope": "global",
        "timeout": 30.0,
        "max_retries": 5,
        "user_agent": "python-utils-64/roblox-sdk-1.0",
        "endpoints": {
            "users": "https://users.roblox.com/v1",
            "games": "https://games.roblox.com/v1",
            "datastore": "https://apis.roblox.com/datastores/v1",
        },
    }

    def __init__(self, config_path: Optional[str] = None, **overrides: Any):
        self._data: Dict[str, Any] = self._deep_copy(self._DEFAULTS)

        if config_path and os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                file_data = json.load(f)
                self._recursive_update(self._data, file_data)

        for key, default_val in self._DEFAULTS.items():
            env_var = f"ROBLOX_{key.upper()}"
            if env_var in os.environ:
                val = os.environ[env_var]
                val_type = type(default_val)
                if val_type is int:
                    self._data[key] = int(val)
                elif val_type is float:
                    self._data[key] = float(val)
                elif val_type is bool:
                    self._data[key] = val.lower() in ("true", "1", "yes")
                else:
                    self._data[key] = val

        self._recursive_update(self._data, overrides)

    def _deep_copy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return json.loads(json.dumps(data))

    def _recursive_update(self, target: Dict[str, Any], source: Dict[str, Any]):
        for k, v in source.items():
            if k in target and isinstance(target[k], dict) and isinstance(v, dict):
                self._recursive_update(target[k], v)
            else:
                target[k] = v

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            val = self._data[name]
            if isinstance(val, dict):
                return type("NestedConfig", (), {k: v for k, v in val.items()})()
            return val
        raise AttributeError(f"'RobloxConfig' object has no attribute '{name}'")

    def __getitem__(self, item: str) -> Any:
        return self._data[item]

    def to_dict(self) -> Dict[str, Any]:
        return self._deep_copy(self._data)
