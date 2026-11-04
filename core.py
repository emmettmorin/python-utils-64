import re
from typing import Dict, List, Iterator, Tuple

class FastRobloxAssetCache:
    """High-performance asset parser and memoized descriptor for Roblox instances."""
    __slots__ = ('_string_pool', '_asset_id_pattern', '_cache')

    def __init__(self) -> None:
        self._string_pool: Dict[str, str] = {}
        self._asset_id_pattern = re.compile(r'(?:rbxassetid://|http://www\.roblox\.com/asset/\?id=)(\d+)')
        self._cache: Dict[int, List[int]] = {}

    def _intern(self, val: str) -> str:
        """Custom string interning pool to reduce memory overhead during large place parsing."""
        return self._string_pool.setdefault(val, val)

    def extract_asset_ids_fast(self, xml_payload: str) -> Iterator[int]:
        """Generator-based fast extraction yielding deduplicated asset IDs directly."""
        seen = set()
        for match in self._asset_id_pattern.finditer(xml_payload):
            asset_id = int(match.group(1))
            if asset_id not in seen:
                seen.add(asset_id)
                yield asset_id

    def batch_process_place(self, place_data: List[str]) -> Dict[int, List[int]]:
        """Chunked pipeline using bitwise hash signatures for fast cache lookups."""
        results: Dict[int, List[int]] = {}
        for idx, chunk in enumerate(place_data):
            chunk_hash = hash(chunk) & 0xFFFFFFFF
            if chunk_hash in self._cache:
                results[idx] = self._cache[chunk_hash]
                continue
            
            ids = list(self.extract_asset_ids_fast(chunk))
            self._cache[chunk_hash] = ids
            results[idx] = ids
        return results

    def warm_cache_from_raw(self, raw_blobs: Tuple[str, ...]) -> None:
        """Pre-warms the internal token pool using generator map evaluation."""
        list(map(self.batch_process_place, ([blob] for blob in raw_blobs)))

    def clear(self) -> None:
        self._string_pool.clear()
        self._cache.clear()