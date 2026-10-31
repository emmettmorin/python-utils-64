import struct
from functools import lru_cache
from typing import List, Tuple, Dict

class RobloxBinaryBuffer:
    __slots__ = ("_view", "_cursor", "_string_cache")

    def __init__(self, data: bytes):
        self._view = memoryview(data)
        self._cursor = 0
        self._string_cache: Dict[int, str] = {}

    @lru_cache(maxsize=2048)
    def _decode_bytes(self, raw_bytes: bytes) -> str:
        return raw_bytes.decode("utf-8", errors="replace")

    def read_int32(self) -> int:
        val = struct.unpack_from("<i", self._view, self._cursor)[0]
        self._cursor += 4
        return val

    def read_fast_string(self) -> str:
        length = self.read_int32()
        if length <= 0 or self._cursor + length > len(self._view):
            return ""
        start = self._cursor
        self._cursor += length
        raw = bytes(self._view[start:self._cursor])
        str_hash = hash(raw)
        if str_hash not in self._string_cache:
            self._string_cache[str_hash] = self._decode_bytes(raw)
        return self._string_cache[str_hash]

    def parse_chunk_headers(self, count: int) -> List[Tuple[int, str]]:
        headers = []
        for _ in range(count):
            if self._cursor + 4 > len(self._view):
                break
            inst_id = self.read_int32()
            name = self.read_fast_string()
            headers.append((inst_id, name))
        return headers
