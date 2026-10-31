import math
from typing import Dict, List, Tuple, Any, Optional

class Vector3Fast:
    __slots__ = ('x', 'y', 'z', '_hash')

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
        self._hash: Optional[int] = None

    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def spatial_key(self, cell_size: float = 4.0) -> int:
        if self._hash is None:
            cx = int(self.x // cell_size) & 0x1FFFFF
            cy = int(self.y // cell_size) & 0xFFFFF
            cz = int(self.z // cell_size) & 0x1FFFFF
            self._hash = (cx << 41) | (cy << 21) | cz
        return self._hash

class SpatialPartitionEngine:
    """High-performance bitwise spatial grid for Roblox workspace part queries."""
    def __init__(self, cell_size: float = 4.0):
        self.cell_size = cell_size
        self._grid: Dict[int, List[Tuple[Vector3Fast, Any]]] = {}

    def insert(self, position: Vector3Fast, payload: Any) -> None:
        key = position.spatial_key(self.cell_size)
        if key not in self._grid:
            self._grid[key] = []
        self._grid[key].append((position, payload))

    def query_radius(self, center: Vector3Fast, radius: float) -> List[Any]:
        r_cells = int(math.ceil(radius / self.cell_size))
        cx = int(center.x // self.cell_size)
        cy = int(center.y // self.cell_size)
        cz = int(center.z // self.cell_size)
        r_sq = radius * radius
        results = []

        for dx in range(-r_cells, r_cells + 1):
            for dy in range(-r_cells, r_cells + 1):
                for dz in range(-r_cells, r_cells + 1):
                    k = (((cx + dx) & 0x1FFFFF) << 41) | (((cy + dy) & 0xFFFFF) << 21) | ((cz + dz) & 0x1FFFFF)
                    bucket = self._grid.get(k)
                    if not bucket:
                        continue
                    for pos, item in bucket:
                        dist_sq = (pos.x - center.x)**2 + (pos.y - center.y)**2 + (pos.z - center.z)**2
                        if dist_sq <= r_sq:
                            results.append(item)
        return results