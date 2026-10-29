import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic attribute-based configuration loader for roblox integration."""
    def __init__(self, defaults: Dict[str, Any], path: str = 'config.json'):
        self._path = path
        self._data = defaults.copy()
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        if os.path.exists(self._path):
            with open(self._path, 'r') as f:
                try:
                    user_cfg = json.load(f)
                    self._data.update(user_cfg)
                except json.JSONDecodeError:
                    pass

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f'Config key {name} not found')

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def save(self) -> None:
        with open(self._path, 'w') as f:
            json.dump(self._data, f, indent=4)

# Usage example for roblox project utility
settings = ConfigLoader({
    'api_key': 'default_key',
    'rate_limit': 60,
    'debug_mode': False
})