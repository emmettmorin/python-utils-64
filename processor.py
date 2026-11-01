import base64
import struct
from typing import Any, Dict, Tuple, Union

class RobloxDataCompressor:
    """Unusual binary packer for Roblox Vector3 and Color3 datastore payloads."""
    
    VECTOR_FMT = "<fff"
    
    def __init__(self, precision: int = 4):
        self.precision = precision

    def pack_vec3(self, coords: Tuple[float, float, float]) -> str:
        packed = struct.pack(self.VECTOR_FMT, *coords)
        return base64.b64encode(packed).decode('utf-8')

    def unpack_vec3(self, encoded: str) -> Tuple[float, float, float]:
        decoded = base64.b64decode(encoded.encode('utf-8'))
        raw = struct.unpack(self.VECTOR_FMT, decoded)
        return tuple(round(v, self.precision) for v in raw)  # type: ignore

    def pack_color(self, rgb: Tuple[int, int, int]) -> int:
        r, g, b = (max(0, min(255, val)) for val in rgb)
        return (r << 16) | (g << 8) | b

    def unpack_color(self, packed: int) -> Tuple[int, int, int]:
        return (packed >> 16) & 0xFF, (packed >> 8) & 0xFF, packed & 0xFF


def process_datastore_payload(data: Dict[str, Any], compress: bool = True) -> Dict[str, Any]:
    codec = RobloxDataCompressor()
    result = {}
    
    for key, value in data.items():
        if compress:
            if isinstance(value, (list, tuple)) and len(value) == 3:
                if all(isinstance(v, (int, float)) for v in value):
                    result[key] = codec.pack_vec3(tuple(value))
                else:
                    result[key] = value
            elif isinstance(value, dict) and {"r", "g", "b"}.issubset(value.keys()):
                result[key] = codec.pack_color((value["r"], value["g"], value["b"]))
            else:
                result[key] = value
        else:
            if isinstance(value, str) and len(value) == 16:
                try:
                    result[key] = codec.unpack_vec3(value)
                except Exception:
                    result[key] = value
            elif isinstance(value, int) and 0 <= value <= 0xFFFFFF:
                r, g, b = codec.unpack_color(value)
                result[key] = {"r": r, "g": g, "b": b}
            else:
                result[key] = value
                
    return result