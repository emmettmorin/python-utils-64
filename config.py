import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str, defaults: Dict[str, Any]):
        self.path = path
        self.defaults = defaults
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            self._save(self.defaults)
            return self.defaults
        with open(self.path, 'r') as f:
            try:
                loaded = json.load(f)
                return {**self.defaults, **loaded}
            except json.JSONDecodeError:
                return self.defaults

    def _save(self, data: Dict[str, Any]) -> None:
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def update(self, key: str, value: Any) -> None:
        self.data[key] = value
        self._save(self.data)

    def __getitem__(self, item: str) -> Any:
        return self.data[item]

    def __repr__(self) -> str:
        return f"Config(path='{self.path}', data={self.data})"