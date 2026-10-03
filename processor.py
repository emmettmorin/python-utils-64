import json
import re
from typing import Any, Dict, Union, Generator

class RobloxAttributeTransformer:
    """Dynamic descriptor for normalizing Roblox property casing and types."""
    def __init__(self, key: str, default: Any = None):
        self.key = key
        self.default = default

    def __get__(self, instance, owner):
        if instance is None:
            return self
        val = instance._raw_data.get(self.key, self.default)
        if isinstance(val, str) and val.isdigit():
            return int(val)
        return val

class InstanceDataProcessor:
    """Cleans and reorganizes raw Roblox web API or place hierarchy payloads."""
    
    asset_id = RobloxAttributeTransformer("TargetId", 0)
    creator_id = RobloxAttributeTransformer("CreatorTargetId", 0)
    name = RobloxAttributeTransformer("Name", "Untitled")

    def __init__(self, raw_payload: Union[str, Dict[str, Any]]):
        if isinstance(raw_payload, str):
            self._raw_data = json.loads(raw_payload)
        else:
            self._raw_data = raw_payload.copy()

    def sanitize_properties(self) -> Dict[str, Any]:
        """Recursively strips Roblox internal XML/JSON tags and cleans string fields."""
        def _clean(val: Any) -> Any:
            if isinstance(val, str):
                return re.sub(r'<[^>]+>', '', val).strip()
            elif isinstance(val, dict):
                return {k.lstrip('@'): _clean(v) for k, v in val.items() if not k.startswith('__')}
            elif isinstance(val, list):
                return [_clean(item) for item in val]
            return val

        return _clean(self._raw_data)

    def normalize_hierarchy(self) -> Generator[Dict[str, Any], None, None]:
        """Flattens nested Roblox instance trees into streamable items."""
        cleaned = self.sanitize_properties()
        stack = [cleaned]
        
        while stack:
            current = stack.pop()
            children = current.pop("Children", []) or current.pop("children", [])
            yield current
            if isinstance(children, list):
                stack.extend(children)