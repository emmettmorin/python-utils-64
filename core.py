import struct
from typing import Dict, Tuple, Any

class FastRobloxVectorBuffer:
    """High-throughput vector serializer utilizing a pre-allocated bytearray buffer."""
    __slots__ = ('_buffer', '_view', '_cursor', '_cache')

    def __init__(self, capacity: int = 1024):
        self._buffer = bytearray(capacity * 12)
        self._view = memoryview(self._buffer)
        self._cursor = 0
        self._cache: Dict[Tuple[float, float, float], int] = {}

    def pack_vector3(self, x: float, y: float, z: float) -> int:
        key = (x, y, z)
        if key in self._cache:
            return self._cache[key]

        offset = self._cursor
        if offset + 12 > len(self._buffer):
            self._buffer.extend(bytearray(len(self._buffer)))
            self._view = memoryview(self._buffer)

        struct.pack_into('<fff', self._view, offset, x, y, z)
        self._cursor += 12
        self._cache[key] = offset
        return offset

    def unpack_vector3(self, offset: int) -> Tuple[float, float, float]:
        return struct.unpack_from('<fff', self._view, offset)

    def bulk_pack(self, vectors: list[Tuple[float, float, float]]) -> memoryview:
        for vec in vectors:
            self.pack_vector3(*vec)
        return self._view[:self._cursor]

    def clear(self) -> None:
        self._cursor = 0
        self._cache.clear()

_GLOBAL_BUFFER = FastRobloxVectorBuffer()

def optimize_roblox_telemetry(instance_data: list[Dict[str, Any]]) -> bytes:
    """Compresses Roblox instance spatial coordinates using zero-copy memory buffers."""
    _GLOBAL_BUFFER.clear()
    for item in instance_data:
        if "Position" in item:
            pos = item["Position"]
            item["_pos_offset"] = _GLOBAL_BUFFER.pack_vector3(pos[0], pos[1], pos[2])
    return bytes(_GLOBAL_BUFFER._view[:_GLOBAL_BUFFER._cursor])
