import os
from typing import Any, Dict

class RobloxConfig:
    __slots__ = ('_settings', 'env')
    
    def __init__(self, workspace: str = 'default'):
        self.env = workspace
        self._settings: Dict[str, Any] = {
            'api_base': 'https://api.roblox.com',
            'throttle_ms': 500,
            'retries': 3,
            'debug': os.getenv('RBX_DEBUG', 'False') == 'True'
        }

    def __getitem__(self, key: str) -> Any:
        return self._settings.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self._settings[key] = value

    def export(self) -> Dict[str, Any]:
        return {**self._settings, 'workspace': self.env}

    @classmethod
    def load_from_env(cls):
        instance = cls()
        for key in ['throttle_ms', 'retries']:
            val = os.getenv(f'RBX_{key.upper()}')
            if val:
                instance[key] = int(val)
        return instance

def get_default_config() -> RobloxConfig:
    return RobloxConfig.load_from_env()