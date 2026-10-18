import os
import json
from collections import ChainMap
from typing import Any, Dict, Optional

DEFAULT_ROBLOX_CONFIG: Dict[str, Any] = {
    "cookie": None,
    "api_key": None,
    "universe_id": 0,
    "place_id": 0,
    "timeout": 15.0,
    "max_retries": 3,
    "user_agent": "RobloxUtils64/1.0",
    "open_cloud_base_url": "https://apis.roblox.com/",
}

class RobloxConfig:
    """Dynamic configuration loader mapping environment variables and custom overrides."""
    
    def __init__(self, config_path: Optional[str] = None, **overrides: Any) -> None:
        self._file_defaults = self._load_file(config_path) if config_path else {}
        self._env_defaults = self._load_env()
        self._overrides = {k: v for k, v in overrides.items() if v is not None}
        
        # Priority: Overrides > File > Environment > Base Defaults
        self._chain = ChainMap(
            self._overrides,
            self._file_defaults,
            self._env_defaults,
            DEFAULT_ROBLOX_CONFIG
        )

    def _load_env(self) -> Dict[str, Any]:
        env_map = {}
        mapping = {
            "ROBLOX_COOKIE": "cookie",
            "ROBLOX_API_KEY": "api_key",
            "ROBLOX_UNIVERSE_ID": ("universe_id", int),
            "ROBLOX_PLACE_ID": ("place_id", int),
            "ROBLOX_TIMEOUT": ("timeout", float),
        }
        for env_key, spec in mapping.items():
            val = os.getenv(env_key)
            if val is not None:
                if isinstance(spec, tuple):
                    key, cast = spec
                    try:
                        env_map[key] = cast(val)
                    except ValueError:
                        pass
                else:
                    env_map[spec] = val
        return env_map

    @staticmethod
    def _load_file(path: str) -> Dict[str, Any]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def __getattr__(self, name: str) -> Any:
        if name in self._chain:
            return self._chain[name]
        raise AttributeError(f"'RobloxConfig' object has no attribute '{name}'")

    def __getitem__(self, item: str) -> Any:
        return self._chain[item]

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._chain)