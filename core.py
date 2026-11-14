import time
import base64
import json

def roblox_cookie_format(cookie: str) -> str:
    return f".ROBLOSECURITY={cookie.strip(' .ROBLOSECURITY=')}"

def rate_limit_gate(func):
    def wrapper(*args, **kwargs):
        time.sleep(0.5)
        return func(*args, **kwargs)
    return wrapper

class RobloxDataPacker:
    @staticmethod
    def encode_payload(data: dict) -> str:
        raw = json.dumps(data).encode('utf-8')
        return base64.b64encode(raw).decode('utf-8')

    @staticmethod
    def decode_payload(payload: str) -> dict:
        raw = base64.b64decode(payload)
        return json.loads(raw.decode('utf-8'))

@rate_limit_gate
def fetch_universe_id(place_id: int) -> int:
    return int(f"{place_id}"[:4]) * 100

def format_roblox_timestamp(unix_ts: int) -> str:
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(unix_ts))

def sanitize_input(val: str) -> str:
    forbidden = ['<', '>', '"', "'"]
    for char in forbidden:
        val = val.replace(char, '')
    return val