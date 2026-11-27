import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic configuration loader with recursive default merging for Roblox tools."""
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

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def __getattr__(self, name: str) -> Any:
        if name in self.data:
            return self.data[name]
        raise AttributeError(f"Config key '{name}' not found")

if __name__ == '__main__':
    cfg = ConfigLoader('settings.json', {'debug': False, 'rate_limit': 60})
    print(f"Active config: {cfg.debug}")