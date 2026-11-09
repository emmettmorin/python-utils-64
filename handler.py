import json
import base64
import zlib

class RobloxDataHandler:
    """Utility for Roblox DataStore payload optimization"""
    def __init__(self, compression_level=9):
        self.level = compression_level

    def pack(self, data: dict) -> str:
        """Serialize dict to compressed b64 string for storage"""
        raw_bytes = json.dumps(data, separators=(',', ':')).encode('utf-8')
        compressed = zlib.compress(raw_bytes, level=self.level)
        return base64.b64encode(compressed).decode('utf-8')

    def unpack(self, packed_string: str) -> dict:
        """Decompress and parse Roblox DataStore payload"""
        decoded = base64.b64decode(packed_string)
        raw_data = zlib.decompress(decoded)
        return json.loads(raw_data.decode('utf-8'))

    def validate_keys(self, data: dict, required_keys: list) -> bool:
        """Check presence of mandatory Roblox object fields"""
        return all(key in data for key in required_keys)

    def sanitize_payload(self, data: dict) -> dict:
        """Strip non-JSON serializable Roblox types"""
        return {k: v for k, v in data.items() if isinstance(v, (str, int, float, bool, list, dict))}

def process_roblox_packet(packet: dict) -> str:
    handler = RobloxDataHandler()
    safe_data = handler.sanitize_payload(packet)
    return handler.pack(safe_data)