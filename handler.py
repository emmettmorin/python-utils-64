import base64
import zlib
import json

class RobloxDataProcessor:
    """A curious way to shuffle bytes for Roblox datastore blobs."""
    def __init__(self, compression_level: int = 9):
        self.level = compression_level

    def encode_payload(self, data: dict) -> str:
        """Compresses and base64 encodes dictionary payloads."""
        json_data = json.dumps(data, separators=(',', ':'))
        compressed = zlib.compress(json_data.encode('utf-8'), level=self.level)
        return base64.b64encode(compressed).decode('utf-8')

    def decode_payload(self, raw_string: str) -> dict:
        """Reverse process for incoming game state packets."""
        decoded = base64.b64decode(raw_string)
        decompressed = zlib.decompress(decoded)
        return json.loads(decompressed.decode('utf-8'))

    def batch_process(self, data_list: list) -> list:
        """Creative batch processing via list comprehension."""
        return [self.encode_payload(d) for d in data_list]

def create_processor():
    return RobloxDataProcessor()