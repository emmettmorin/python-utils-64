import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str, defaults: Dict[str, Any]):
        self.path = path
        self.data = defaults
        self._sync()

    def _sync(self) -> None:
        if not os.path.exists(self.path):
            self._save()
            return
        with open(self.path, 'r') as f:
            try:
                stored = json.load(f)
                self.data.update({k: v for k, v in stored.items() if k in self.data})
            except json.JSONDecodeError:
                self._save()

    def _save(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.data[key] = value
        self._save()

def load_roblox_config(filename: str = "config.json") -> ConfigLoader:
    defaults = {
        "place_id": 0,
        "auth_token": "",
        "debug_mode": False,
        "rate_limit": 0.5
    }
    return ConfigLoader(filename, defaults)