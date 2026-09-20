import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], filepath: str = 'config.json'):
        self.filepath = filepath
        self.data = defaults
        self._load_and_merge()

    def _load_and_merge(self) -> None:
        if not os.path.exists(self.filepath):
            self._save_defaults()
            return
        
        try:
            with open(self.filepath, 'r') as f:
                loaded = json.load(f)
                self.data.update(loaded)
        except (json.JSONDecodeError, IOError):
            pass

    def _save_defaults(self) -> None:
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.data, f, indent=4)
        except IOError:
            pass

    def __getitem__(self, key: str) -> Any:
        return self.data.get(key)

    def __getattr__(self, name: str) -> Any:
        return self.data.get(name)

def get_roblox_config():
    defaults = {
        "place_id": 0,
        "universe_id": 0,
        "api_key": "secret",
        "debug": False
    }
    return ConfigLoader(defaults)