import json
import base64
import zlib
from typing import Any, Dict

class RobloxDataProcessor:
    """
    A somewhat unusual approach to roblox data packing
    using zlib compression for large JSON payloads.
    """
    @staticmethod
    def encode(data: Dict[str, Any]) -> str:
        json_str = json.dumps(data, separators=(',', ':'))
        compressed = zlib.compress(json_str.encode('utf-8'), level=9)
        return base64.b64encode(compressed).decode('ascii')

    @staticmethod
    def decode(payload: str) -> Dict[str, Any]:
        compressed = base64.b64decode(payload)
        json_str = zlib.decompress(compressed).decode('utf-8')
        return json.loads(json_str)

def sanitize_key(key: str) -> str:
    """
    removes non-alphanumeric chars to satisfy datastore requirements
    """
    return ''.join(c for c in key if c.isalnum())

def format_player_data(player_id: int, stats: Dict[str, Any]) -> Dict[str, Any]:
    """
    wraps stats into a roblox-ready manifest
    """
    return {
        'pid': player_id,
        'data': RobloxDataProcessor.encode(stats),
        'meta': {'v': 1, 'c': 'zlib-base64'}
    }