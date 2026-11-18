import base64
import json
import zlib

class RobloxDataProcessor:
    """Advanced handler for Roblox data serialization and compression."""
    
    @staticmethod
    def serialize(data: dict) -> str:
        """Compress and encode data into Roblox-compatible format."""
        json_str = json.dumps(data, separators=(',', ':'))
        compressed = zlib.compress(json_str.encode('utf-8'), level=9)
        return base64.b64encode(compressed).decode('utf-8')

    @staticmethod
    def deserialize(encoded: str) -> dict:
        """Decode and decompress Roblox-compatible payload."""
        raw = base64.b64decode(encoded)
        decompressed = zlib.decompress(raw)
        return json.loads(decompressed.decode('utf-8'))

    @classmethod
    def sanitize_key(cls, key: str) -> str:
        """Sanitize keys to follow Roblox variable constraints."""
        return "".join(c if c.isalnum() else "_" for c in key)[:50]

    def process_bundle(self, data_list: list) -> list:
        """Batch processing for multi-packet data streams."""
        return [self.serialize(item) for item in data_list]

if __name__ == '__main__':
    handler = RobloxDataProcessor()
    sample = {'level': 5, 'items': ['sword', 'shield']}
    packed = handler.serialize(sample)
    print(f'Encoded: {packed}')
    assert handler.deserialize(packed) == sample