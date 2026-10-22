import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Magic configuration loader with recursive default merging."""
    def __init__(self, file_path: str, defaults: Dict[str, Any]):
        self.path = file_path
        self.defaults = defaults
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                loaded = json.load(f)
                return {**self.defaults, **loaded}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getattr__(self, item: str) -> Any:
        if item in self.data:
            return self.data[item]
        raise AttributeError(f'Config has no key {item}')

def create_config(path: str, defaults: Dict[str, Any]) -> ConfigLoader:
    """Factory function for global configuration state."""
    return ConfigLoader(path, defaults)