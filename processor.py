import struct
import base64
from typing import Dict, Any, Tuple, Union

class RobloxDataProcessor:
    """Processor for packing and unpacking Roblox spatial structures for DataStores."""

    _VEC3_FMT = "<fff"
    _CFRAME_FMT = "<ffffffffffff"

    @classmethod
    def pack_vector3(cls, x: float, y: float, z: float) -> str:
        raw = struct.pack(cls._VEC3_FMT, float(x), float(y), float(z))
        return base64.b64encode(raw).decode("ascii")

    @classmethod
    def unpack_vector3(cls, b64_str: str) -> Tuple[float, float, float]:
        raw = base64.b64decode(b64_str.encode("ascii"))
        if len(raw) != struct.calcsize(cls._VEC3_FMT):
            raise ValueError("Invalid buffer size for Roblox Vector3")
        return struct.unpack(cls._VEC3_FMT, raw)

    @classmethod
    def pack_cframe(cls, components: Tuple[float, ...]) -> str:
        if len(components) != 12:
            raise ValueError("CFrame requires exactly 12 component values")
        raw = struct.pack(cls._CFRAME_FMT, *[float(c) for c in components])
        return base64.b64encode(raw).decode("ascii")

    @classmethod
    def unpack_cframe(cls, b64_str: str) -> Tuple[float, ...]:
        raw = base64.b64decode(b64_str.encode("ascii"))
        if len(raw) != struct.calcsize(cls._CFRAME_FMT):
            raise ValueError("Invalid buffer size for Roblox CFrame")
        return struct.unpack(cls._CFRAME_FMT, raw)

    @classmethod
    def sanitize_datastore_payload(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        cleaned = {}
        for key, val in payload.items():
            if isinstance(val, (list, tuple)) and len(val) == 3:
                cleaned[key] = {"_rbx_type": "Vector3", "b64": cls.pack_vector3(*val)}
            elif isinstance(val, (list, tuple)) and len(val) == 12:
                cleaned[key] = {"_rbx_type": "CFrame", "b64": cls.pack_cframe(val)}
            elif isinstance(val, dict):
                cleaned[key] = cls.sanitize_datastore_payload(val)
            else:
                cleaned[key] = val
        return cleaned
