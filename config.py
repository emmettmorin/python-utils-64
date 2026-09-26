import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, file_path: str, defaults: Dict[str, Any]):
        self.path = file_path
        self.data = defaults
        self._sync()

    def _sync(self) -> None:
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                try:
                    user_data = json.load(f)
                    self.data.update(user_data)
                except json.JSONDecodeError:
                    pass
        else:
            self._save()

    def _save(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self._save()

def load_roblox_config(filename: str = 'settings.json') -> ConfigLoader:
    defaults = {
        "place_id": 0,
        "auth_token": "",
        "request_delay": 0.5,
        "debug_mode": False
    }
    return ConfigLoader(filename, defaults)