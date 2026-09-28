import re
from typing import Union, Tuple, Dict, Any

class Color3Packed:
    """Utility for packed 24-bit RGB and Roblox Color3 normalization."""
    def __init__(self, r: float, g: float, b: float):
        self.r = max(0.0, min(1.0, r))
        self.g = max(0.0, min(1.0, g))
        self.b = max(0.0, min(1.0, b))

    @classmethod
    def from_hex(cls, hex_str: str) -> "Color3Packed":
        clean = hex_str.lstrip('#')
        val = int(clean, 16)
        return cls(((val >> 16) & 0xFF) / 255.0, ((val >> 8) & 0xFF) / 255.0, (val & 0xFF) / 255.0)

    @classmethod
    def from_rgb255(cls, r: int, g: int, b: int) -> "Color3Packed":
        return cls(r / 255.0, g / 255.0, b / 255.0)

    def to_rgb255(self) -> Tuple[int, int, int]:
        return (round(self.r * 255), round(self.g * 255), round(self.b * 255))

    def pack_int(self) -> int:
        r, g, b = self.to_rgb255()
        return (r << 16) | (g << 8) | b

    def __repr__(self) -> str:
        return f"Color3({self.r:.3f}, {self.g:.3f}, {self.b:.3f})"


class AssetResolver:
    """Helper for converting Roblox asset IDs and constructing API endpoints."""
    BASE_ASSET_URL = "https://assetdelivery.roblox.com/v1/asset/?id="
    BASE_GAME_URL = "https://games.roblox.com/v1/games"

    def __init__(self, target: Union[int, str]):
        self.raw_target = str(target)
        self.id = self._extract_id(self.raw_target)

    @staticmethod
    def _extract_id(val: str) -> int:
        match = re.search(r'\d+', val)
        if not match:
            raise ValueError(f"Invalid Roblox ID source: {val}")
        return int(match.group(0))

    def to_asset_url(self) -> str:
        return f"{self.BASE_ASSET_URL}{self.id}"

    def to_place_detail_endpoint(self) -> str:
        return f"{self.BASE_GAME_URL}?placeIds={self.id}"

    def __matmul__(self, asset_type: str) -> Dict[str, Any]:
        return {"id": self.id, "type": asset_type, "url": self.to_asset_url()}
