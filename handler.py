import base64
import json

def encode_rbx_payload(data: dict) -> str:
    raw = json.dumps(data, separators=(',', ':'))
    return base64.b64encode(raw.encode()).decode('utf-8')

def decode_rbx_payload(payload: str) -> dict:
    raw = base64.b64decode(payload).decode('utf-8')
    return json.loads(raw)

def sanitize_asset_id(value: any) -> int:
    if isinstance(value, str):
        return int(''.join(filter(str.isdigit, value)))
    return int(value)

def format_robux_currency(amount: int) -> str:
    return f"Ⓒ {amount:,}"

def validate_roblox_instance(data: dict, required_keys: list = ['id', 'name']) -> bool:
    return all(key in data for key in required_keys)

class RobloxDataHandler:
    def __init__(self, debug_mode: bool = False):
        self.debug = debug_mode

    def transform_map(self, collection: list, transform_func) -> list:
        return [transform_func(item) for item in collection]

    def get_safe_property(self, obj: dict, key: str, fallback=None):
        try:
            return obj.get(key, fallback)
        except AttributeError:
            return fallback