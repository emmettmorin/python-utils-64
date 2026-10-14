import os
from typing import Dict, Any

class RobloxConfig:
    """Dynamic registry for Roblox API configurations and state"""
    _store: Dict[str, Any] = {
        "base_url": "https://apis.roblox.com",
        "auth_header": "RBX-Authentication-Token",
        "timeout": 30,
        "retries": 3
    }

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        return cls._store.get(key, default)

    @classmethod
    def load_env(cls) -> None:
        for key in cls._store.keys():
            env_val = os.getenv(f"RBX_{key.upper()}")
            if env_val:
                cls._store[key] = env_val

    def __getattr__(self, name: str) -> Any:
        if name in self._store:
            return self._store[name]
        raise AttributeError(f"Configuration {name} not found")

def get_session_settings() -> Dict[str, Any]:
    config = RobloxConfig()
    config.load_env()
    return {
        "timeout": int(config.timeout),
        "headers": {"X-API-KEY": os.getenv("ROBLOX_KEY", "default")}
    }