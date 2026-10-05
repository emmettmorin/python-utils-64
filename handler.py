import base64
import json
import zlib

class RobloxDataProcessor:
    """Handles mysterious Roblox blob transformation for 64-bit architecture"""

    @staticmethod
    def serialize_game_state(data: dict) -> str:
        # Convert dict to JSON string then compress with zlib for efficiency
        raw_bytes = json.dumps(data).encode('utf-8')
        compressed = zlib.compress(raw_bytes, level=9)
        return base64.b85encode(compressed).decode('ascii')

    @staticmethod
    def deserialize_game_state(blob: str) -> dict:
        # Decompress 64-bit compatible blob back to dictionary
        compressed = base64.b85decode(blob.encode('ascii'))
        raw_data = zlib.decompress(compressed)
        return json.loads(raw_data.decode('utf-8'))

    @classmethod
    def sanitize_input(cls, payload: any) -> dict:
        """Wraps raw input into standard Roblox-ready schema"""
        if not isinstance(payload, dict):
            payload = {'payload': payload, 'type': 'raw'}
        
        payload.setdefault('timestamp', 0)
        payload.setdefault('meta', {'origin': 'python-utils-64'})
        return payload

def fast_encode(data: dict) -> str:
    handler = RobloxDataProcessor()
    clean_data = handler.sanitize_input(data)
    return handler.serialize_game_state(clean_data)

def fast_decode(blob: str) -> dict:
    handler = RobloxDataProcessor()
    return handler.deserialize_game_state(blob)