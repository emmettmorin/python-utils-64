import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic configuration loader for roblox utility scripts."""
    def __init__(self, filepath: str, defaults: Dict[str, Any]):
        self.filepath = filepath
        self.defaults = defaults
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.filepath):
            self._save(self.defaults)
            return self.defaults
        try:
            with open(self.filepath, 'r') as f:
                return {**self.defaults, **json.load(f)}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def _save(self, data: Dict[str, Any]) -> None:
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def __getitem__(self, key: str) -> Any:
        return self.data.get(key, self.defaults.get(key))

    def update(self, key: str, value: Any) -> None:
        self.data[key] = value
        self._save(self.data)

    @property
    def raw(self) -> Dict[str, Any]:
        return self.data

def get_roblox_config(path: str = "config.json") -> ConfigLoader:
    defaults = {
        "api_key": "",
        "place_id": 0,
        "debug_mode": False,
        "rate_limit": 0.5
    }
    return ConfigLoader(path, defaults)