import re
from typing import Any, Optional

class RobloxIDValidator:
    """Validator suite for Roblox-related resource identifiers."""
    
    _PATTERN = re.compile(r'^\d+$')

    @classmethod
    def is_valid_asset(cls, asset_id: Any) -> bool:
        try:
            return bool(cls._PATTERN.match(str(asset_id)))
        except (TypeError, ValueError):
            return False

    @classmethod
    def sanitize_input(cls, value: Any) -> Optional[int]:
        """Cast messy inputs into strict integer IDs."""
        str_val = str(value).strip()
        if cls._PATTERN.match(str_val):
            return int(str_val)
        return None

def validate_roblox_instance(data: dict) -> bool:
    """Duck-typing check for Roblox API object structure."""
    required_keys = {'AssetId', 'CreatorType', 'Price'}
    return all(key in data for key in required_keys)

class DataSanitizer:
    """Chainable processing for Roblox metadata payloads."""
    def __init__(self, data: dict):
        self.data = data

    def strip_nil(self) -> 'DataSanitizer':
        self.data = {k: v for k, v in self.data.items() if v is not None}
        return self