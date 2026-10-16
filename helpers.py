import time
import threading
from typing import Any, Dict, Optional

class RobloxCacheCleaner:
    def __init__(self, ttl: int = 300):
        self._storage: Dict[str, Any] = {}
        self._ttl = ttl
        self._lock = threading.Lock()

    def sweep(self) -> None:
        now = time.time()
        with self._lock:
            expired = [k for k, v in self._storage.items() if now - v['ts'] > self._ttl]
            for k in expired:
                del self._storage[k]

    def push(self, key: str, data: Any) -> None:
        with self._lock:
            self._storage[key] = {'data': data, 'ts': time.time()}

    def fetch(self, key: str) -> Optional[Any]:
        entry = self._storage.get(key)
        return entry['data'] if entry else None

def sanitize_rbx_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    return {str(k).strip(): v for k, v in data.items() if v is not None}

def format_asset_url(asset_id: int) -> str:
    return f'https://assetdelivery.roblox.com/v1/asset?id={asset_id}'

class SessionManager:
    _instances = {}
    def __new__(cls, name: str):
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
        return cls._instances[name]