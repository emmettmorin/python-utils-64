import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], path: str = 'config.json'):
        self.path = path
        self.data = defaults
        self._load_and_merge()

    def _load_and_merge(self) -> None:
        if not os.path.exists(self.path):
            self._save_defaults()
            return
        
        try:
            with open(self.path, 'r') as f:
                loaded = json.load(f)
                self.data.update({k: v for k, v in loaded.items() if k in self.data})
        except (json.JSONDecodeError, IOError):
            pass

    def _save_defaults(self) -> None:
        try:
            with open(self.path, 'w') as f:
                json.dump(self.data, f, indent=4)
        except IOError:
            pass

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name)

def get_roblox_config(defaults: Dict[str, Any]) -> ConfigLoader:
    return ConfigLoader(defaults, 'roblox_settings.json')