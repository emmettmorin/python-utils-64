import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, file_path: str, defaults: Dict[str, Any] = None):
        self.path = file_path
        self.defaults = defaults or {}
        self.config = self._initialize()

    def _initialize(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                json.dump(self.defaults, f, indent=4)
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
            return {**self.defaults, **data}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.config[key]

    def reload(self):
        self.config = self._initialize()

    def __getattr__(self, name: str) -> Any:
        if name in self.config:
            return self.config[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")