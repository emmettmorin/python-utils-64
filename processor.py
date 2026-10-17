import base64
import json
import zlib

def encode_roblox_data(data: dict) -> str:
    """Compresses and base64 encodes a dictionary for Roblox storage."""
    raw_json = json.dumps(data, separators=(',', ':'))
    compressed = zlib.compress(raw_json.encode('utf-8'))
    return base64.b64encode(compressed).decode('utf-8')

def decode_roblox_data(blob: str) -> dict:
    """Decodes and decompress a Roblox datastore blob."""
    raw_bytes = base64.b64decode(blob)
    decompressed = zlib.decompress(raw_bytes)
    return json.loads(decompressed.decode('utf-8'))

class RobloxDataContainer:
    """Creative wrapper for structured data transport."""
    def __init__(self, key: str):
        self.key = key

    def serialize(self, payload: dict) -> dict:
        return {
            "k": self.key,
            "v": encode_roblox_data(payload),
            "c": 1
        }

    def deserialize(self, container: dict) -> dict:
        if container.get("c") != 1:
            raise ValueError("incompatible container version")
        return decode_roblox_data(container["v"])