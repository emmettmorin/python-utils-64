import base64
import zlib
import json

class RobloxDataBridge:
    """Encapsulates unusual serialization for Roblox DataStore keys."""
    def __init__(self, salt: str = "rbx-secure"):
        self.salt = salt

    def encode_payload(self, data: dict) -> str:
        raw = json.dumps(data, separators=(',', ':'))
        compressed = zlib.compress(raw.encode() + self.salt.encode())
        return base64.urlsafe_b64encode(compressed).decode('ascii')

    def decode_payload(self, payload: str) -> dict:
        raw_data = base64.urlsafe_b64decode(payload.encode())
        decompressed = zlib.decompress(raw_data).decode('utf-8')
        return json.loads(decompressed.replace(self.salt, ""))

    @staticmethod
    def sanitize_key(key: str) -> str:
        """Forces Roblox-friendly key constraints."""
        return "".join([c for c in key if c.isalnum() or c in "_-"])[:50]

def wrap_datastore_packet(data: dict) -> dict:
    bridge = RobloxDataBridge()
    return {
        "payload": bridge.encode_payload(data),
        "timestamp": bridge.sanitize_key("v1"),
        "checksum": hash(str(data)) % 1000
    }