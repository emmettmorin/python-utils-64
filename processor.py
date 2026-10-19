import json
from typing import Any, Callable, Dict, Union

class RobloxDataProcessor:
    """Creative transformer for Roblox DataStore and place payload structures."""

    def __init__(self) -> None:
        self._transformers: Dict[str, Callable[[Any], Any]] = {
            "Vector3": lambda d: tuple(float(d.get(k, 0.0)) for k in ("X", "Y", "Z")),
            "Color3": lambda d: f"#{int(d.get('R', 0) * 255):02x}{int(d.get('G', 0) * 255):02x}{int(d.get('B', 0) * 255):02x}",
            "CFrame": lambda d: {
                "pos": tuple(float(d.get("Position", {}).get(k, 0.0)) for k in ("X", "Y", "Z")),
                "rot": d.get("Rotation", [1, 0, 0, 0, 1, 0, 0, 0, 1])
            }
        }

    def register_type(self, type_name: str, fn: Callable[[Any], Any]) -> None:
        self._transformers[type_name] = fn

    def process_node(self, data: Any) -> Any:
        if isinstance(data, dict):
            if "__type" in data and data["__type"] in self._transformers:
                return self._transformers[data["__type"]](data)
            return {k: self.process_node(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.process_node(item) for item in data]
        return data

    def unpack_attributes(self, raw_payload: Union[str, bytes, dict]) -> dict:
        if isinstance(raw_payload, (str, bytes)):
            parsed = json.loads(raw_payload)
        else:
            parsed = raw_payload
        
        processed = self.process_node(parsed)
        if isinstance(processed, dict):
            processed["_meta"] = {"processed_keys": len(processed)}
        return processed
