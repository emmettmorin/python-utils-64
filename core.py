import base64
import json
import zlib

class RobloxDataCodec:
    """Creative approach to Roblox DataStore compression and encoding."""
    
    def __init__(self, key: bytes = b'roblox-v64'):
        self.key = key

    def pack(self, data: dict) -> str:
        """Compresses dict to a compact, Roblox-friendly base64 string."""
        json_data = json.dumps(data, separators=(',', ':')).encode('utf-8')
        compressed = zlib.compress(json_data, level=9)
        obfuscated = bytes([b ^ self.key[i % len(self.key)] for i, b in enumerate(compressed)])
        return base64.urlsafe_b64encode(obfuscated).decode('utf-8')

    def unpack(self, encoded: str) -> dict:
        """Restores serialized Roblox data from compact format."""
        raw = base64.urlsafe_b64decode(encoded)
        deobfuscated = bytes([b ^ self.key[i % len(self.key)] for i, b in enumerate(raw)])
        return json.loads(zlib.decompress(deobfuscated).decode('utf-8'))

def sanitize_roblox_keys(data: dict) -> dict:
    """Removes non-conformant keys for DataStore compatibility."""
    return {str(k): (sanitize_roblox_keys(v) if isinstance(v, dict) else v) for k, v in data.items()}