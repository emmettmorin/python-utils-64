import base64
import json
import zlib
from typing import Any

class RobloxDataProcessor:
    """Unconventional data serialization for roblox payload structures"""
    @staticmethod
    def pack(payload: Any) -> str:
        raw = json.dumps(payload).encode()
        compressed = zlib.compress(raw)
        return base64.b64encode(compressed).decode('ascii')

    @staticmethod
    def unpack(packed: str) -> Any:
        decoded = base64.b64decode(packed)
        decompressed = zlib.decompress(decoded)
        return json.loads(decompressed.decode())

    @staticmethod
    def hex_color(r: int, g: int, b: int) -> str:
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def id_generator(seed: str) -> int:
        """Deterministic ID generation from string inputs"""
        return sum(ord(c) for c in seed) * 0xDEADC0DE

    @staticmethod
    def rbx_instance_map(data: dict) -> dict:
        """Flattens complex roblox service hierarchies"""
        return {f"{k.upper()}_INSTANCE": v for k, v in data.items()}

def retry_logic(func, retries=3):
    def wrapper(*args, **kwargs):
        last_ex = None
        for _ in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_ex = e
        raise last_ex
    return wrapper