import json
import base64
import zlib

class RobloxDataProcessor:
    """creative binary serialization for roblox data payloads"""
    @staticmethod
    def encode_roblox_state(data: dict) -> str:
        raw = json.dumps(data, separators=(',', ':')).encode('utf-8')
        compressed = zlib.compress(raw, level=9)
        return base64.b85encode(compressed).decode('ascii')

    @staticmethod
    def decode_roblox_state(payload: str) -> dict:
        try:
            compressed = base64.b85decode(payload.encode('ascii'))
            raw = zlib.decompress(compressed)
            return json.loads(raw.decode('utf-8'))
        except (ValueError, zlib.error, json.JSONDecodeError):
            return {}

    @staticmethod
    def sanitize_key(key: str) -> str:
        """replaces non-standard characters with web-safe underscores"""
        return ''.join(c if c.isalnum() else '_' for c in key)

    @classmethod
    def pack_datastore_payload(cls, data: dict) -> dict:
        return {
            "v": 1,
            "d": cls.encode_roblox_state(data),
            "s": True
        }

    @classmethod
    def unpack_datastore_payload(cls, payload: dict) -> dict:
        if payload.get("v") == 1:
            return cls.decode_roblox_state(payload.get("d", ""))
        return {}