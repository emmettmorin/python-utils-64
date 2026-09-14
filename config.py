import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, file_path: str, defaults: Dict[str, Any]):
        self.path = file_path
        self.defaults = defaults
        self._data = self.load()

    def load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults.copy()
        with open(self.path, 'r') as f:
            try:
                data = json.load(f)
                return {**self.defaults, **data}
            except (json.JSONDecodeError, IOError):
                return self.defaults.copy()

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self._data, f, indent=4)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f'Config has no attribute {name}')