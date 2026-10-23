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
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                file_data = json.load(f)
                return {**self.defaults, **file_data}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

class RobloxConfig(ConfigLoader):
    def __init__(self, settings_path: str = "config.json"):
        defaults = {
            "place_id": 0,
            "universe_id": 0,
            "api_key": "",
            "environment": "production"
        }
        super().__init__(settings_path, defaults)

    def sync_with_env(self):
        for key in self.data:
            env_val = os.getenv(f"RBX_{key.upper()}")
            if env_val:
                self.data[key] = env_val