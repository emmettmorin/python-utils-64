import time
import json
from typing import Any, Callable

def roblox_id_sanitizer(raw_input: Any) -> int:
    try:
        return int(str(raw_input).split('/')[-1])
    except (ValueError, IndexError):
        return 0

def retry_request(attempts: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (i + 1))
            raise last_ex
        return wrapper
    return decorator

def rbx_payload_builder(action: str, **kwargs) -> str:
    return json.dumps({"meta": {"origin": "python-utils-64", "ts": time.time()}, "task": action, "data": kwargs})

class RobloxSessionData:
    def __init__(self, cookie: str):
        self.cookie = f".ROBLOSECURITY={cookie}"

    def get_headers(self) -> dict:
        return {"Cookie": self.cookie, "User-Agent": "Roblox/WinInet"}

def pluck_user_data(payload: dict, keys: list) -> dict:
    return {k: payload.get(k) for k in keys if k in payload}