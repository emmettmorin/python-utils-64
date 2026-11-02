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
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get(self, key: str, fallback: Any = None) -> Any:
        return self.data.get(key, fallback)

def get_roblox_config() -> ConfigLoader:
    defaults = {
        "place_id": 0,
        "api_key": "sk-hidden",
        "rate_limit": 60,
        "debug_mode": True
    }
    return ConfigLoader(defaults)

if __name__ == '__main__':
    cfg = get_roblox_config()
    print(f"Active session for place: {cfg.get('place_id')}")