import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, file_path: str, defaults: Dict[str, Any]):
        self.path = file_path
        self.data = defaults.copy()
        self._load_and_merge()

    def _load_and_merge(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    disk_data = json.load(f)
                    self.data.update(disk_data)
            except (json.JSONDecodeError, IOError):
                pass

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ['path', 'data']:
            super().__setattr__(name, value)
        else:
            self.data[name] = value
            self._save()

    def _save(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

def get_roblox_config(path: str = 'settings.json') -> ConfigLoader:
    defaults = {
        "universe_id": 0,
        "api_key": "",
        "throttle_limit": 60,
        "debug_mode": False
    }
    return ConfigLoader(path, defaults)