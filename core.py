import math
from typing import Tuple, List, Generator

class Vector3Pool:
    """Object recycling pool for high-throughput Roblox mesh processing."""
    __slots__ = ('_pool', '_max_size')

    def __init__(self, max_size: int = 10000):
        self._pool: List[Tuple[float, float, float]] = []
        self._max_size = max_size

    def acquire(self, x: float, y: float, z: float) -> Tuple[float, float, float]:
        if self._pool:
            self._pool.pop()
        return (float(x), float(y), float(z))

    def release(self, vec: Tuple[float, float, float]) -> None:
        if len(self._pool) < self._max_size:
            self._pool.append(vec)


class FastCFrame:
    """Optimized unrolled CFrame matrix calculations for spatial transforms."""
    __slots__ = ('pos', 'rot')

    def __init__(self, x: float, y: float, z: float, r00: float = 1.0, r01: float = 0.0, r02: float = 0.0,
                 r10: float = 0.0, r11: float = 1.0, r12: float = 0.0, r20: float = 0.0, r21: float = 0.0, r22: float = 1.0):
        self.pos = (float(x), float(y), float(z))
        self.rot = (r00, r01, r02, r10, r11, r12, r20, r21, r22)

    def batch_transform_points(self, points: List[Tuple[float, float, float]]) -> List[Tuple[float, float, float]]:
        """Fast-path unrolled matrix multiplication for Roblox part vertex streams."""
        px, py, pz = self.pos
        r00, r01, r02, r10, r11, r12, r20, r21, r22 = self.rot
        
        transformed = []
        append = transformed.append
        
        for vx, vy, vz in points:
            append((
                px + (vx * r00 + vy * r01 + vz * r02),
                py + (vx * r10 + vy * r11 + vz * r12),
                pz + (vx * r20 + vy * r21 + vz * r22)
            ))
            
        return transformed

    @classmethod
    def from_euler_angles_xyz(cls, x: float, y: float, z: float, rx: float, ry: float, rz: float) -> 'FastCFrame':
        cx, cy, cz = math.cos(rx), math.cos(ry), math.cos(rz)
        sx, sy, sz = math.sin(rx), math.sin(ry), math.sin(rz)
        return cls(
            x, y, z,
            cy * cz, -cy * sz, sy,
            sx * sy * cz + cx * sz, -sx * sy * sz + cx * cz, -sx * cy,
            -cx * sy * cz + sx * sz, cx * sy * sz + sx * cz, cx * cy
        )
