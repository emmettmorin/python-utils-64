import struct
from functools import lru_cache
from typing import List, Tuple, Generator

class FastCFrameTransformer:
    """Optimized batch CFrame spatial processor for Roblox Vector3 cloud operations."""
    __slots__ = ('_matrix', '_packed_translation')

    def __init__(self, cframe_components: Tuple[float, ...]):
        if len(cframe_components) != 12:
            raise ValueError("CFrame components require exactly 12 float values")
        self._packed_translation = struct.pack('<fff', *cframe_components[:3])
        self._matrix = cframe_components[3:]

    @staticmethod
    @lru_cache(maxsize=2048)
    def _cached_rot_transform(r_tuple: Tuple[float, ...], x: float, y: float, z: float) -> Tuple[float, float, float]:
        r00, r01, r02, r10, r11, r12, r20, r21, r22 = r_tuple
        return (
            r00 * x + r01 * y + r02 * z,
            r10 * x + r11 * y + r12 * z,
            r20 * x + r21 * y + r22 * z
        )

    def transform_point_cloud(self, points: List[Tuple[float, float, float]]) -> bytes:
        tx, ty, tz = struct.unpack('<fff', self._packed_translation)
        matrix = self._matrix
        buf = bytearray(len(points) * 12)
        view = memoryview(buf)
        
        offset = 0
        for px, py, pz in points:
            rx, ry, rz = self._cached_rot_transform(matrix, px, py, pz)
            struct.pack_into('<fff', view, offset, rx + tx, ry + ty, rz + tz)
            offset += 12

        return bytes(buf)

    def unpack_binary_cloud(self, binary_data: bytes) -> Generator[Tuple[float, float, float], None, None]:
        for x, y, z in struct.iter_unpack('<fff', binary_data):
            yield (round(x, 4), round(y, 4), round(z, 4))
