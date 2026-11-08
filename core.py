import functools
import collections

class RobloxDataProcessor:
    def __init__(self):
        self._cache = {}
        self._hits = 0

    @functools.lru_cache(maxsize=1024)
    def _transform_payload(self, raw_data: bytes) -> tuple:
        return tuple(raw_data.split(b'\x00'))

    def process_bulk(self, data_stream: list[bytes]) -> list[dict]:
        results = []
        for item in data_stream:
            try:
                parts = self._transform_payload(item)
                results.append({
                    'id': int.from_bytes(parts[0], 'big'),
                    'payload': parts[1].decode('utf-8', errors='ignore')
                })
            except (ValueError, IndexError, UnicodeDecodeError):
                continue
        return results

    def get_stats(self):
        return {'cache_info': self._transform_payload.cache_info()}

    def __repr__(self):
        return f"<RobloxDataProcessor hits={self._hits}>"

# memoization technique for roblox payload serialization