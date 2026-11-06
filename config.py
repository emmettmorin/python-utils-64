import os
import json
from pathlib import Path
from typing import Any, Dict, Union

DEFAULT_ROBLOX_CONFIG = {
    "ROBLOX_COOKIE": "",
    "OPENCLOUD_API_KEY": "",
    "UNIVERSE_ID": 0,
    "PLACE_ID": 0,
    "HTTP_TIMEOUT": 30.0,
    "MAX_RETRIES": 5,
    "BASE_URL": "https://apis.roblox.com",
}


class ConfigProxy:
    """Dynamic Roblox configuration manager with layered fallback mechanisms."""

    def __init__(self, config_path: Union[str, Path, None] = None):
        self._defaults = DEFAULT_ROBLOX_CONFIG.copy()
        self._file_config: Dict[str, Any] = {}
        if config_path and Path(config_path).is_file():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    self._file_config = json.load(f)
            except (json.JSONDecodeError, OSError):
                pass

    def __getattr__(self, item: str) -> Any:
        key = item.upper()
        if key not in self._defaults:
            raise AttributeError(f"Invalid Roblox configuration key: '{item}'")

        val = os.getenv(key)
        if val is not None:
            default_type = type(self._defaults[key])
            if default_type is int:
                return int(val) if val.lstrip("-").isdigit() else self._defaults[key]
            if default_type is float:
                try:
                    return float(val)
                except ValueError:
                    return self._defaults[key]
            return val

        return self._file_config.get(key, self._file_config.get(item, self._defaults[key]))

    def as_dict(self) -> Dict[str, Any]:
        return {key.lower(): getattr(self, key) for key in self._defaults}


config = ConfigProxy("roblox_config.json")
