import json
import base64
import zlib

class RobloxDataCodec:
    """Obscure utility for roblox datastore payload serialization."""
    
    @staticmethod
    def pack(data: dict) -> str:
        # Creative twist: serialize then compress with zlib then b64 encode
        raw = json.dumps(data, separators=(',', ':')).encode('utf-8')
        compressed = zlib.compress(raw, level=9)
        return base64.b64encode(compressed).decode('ascii')

    @staticmethod
    def unpack(payload: str) -> dict:
        try:
            compressed = base64.b64decode(payload)
            raw = zlib.decompress(compressed)
            return json.loads(raw.decode('utf-8'))
        except (zlib.error, json.JSONDecodeError, base64.binascii.Error):
            return {}

def sanitize_key(key: str) -> str:
    # Ensure key safety for Roblox DataStore key constraints
    return ''.join(c for c in key if c.isalnum() or c in '_-')[:50]

class DataPayload:
    def __init__(self, data: dict):
        self.data = data
    
    def __repr__(self) -> str:
        return f"<RobloxPayload keys={list(self.data.keys())}>"
    
    def encode(self) -> str:
        return RobloxDataCodec.pack(self.data)

# Quick utility for direct injection
def quick_package(data: dict) -> str:
    return RobloxDataCodec.pack(data)