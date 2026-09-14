import re
from typing import Any, Union

class RobloxValidator:
    """Utility suite for Roblox-specific data validation."""
    
    @staticmethod
    def validate_asset_id(asset_id: Any) -> int:
        target = str(asset_id)
        if not target.isdigit():
            raise ValueError(f"Invalid Asset ID format: {target}")
        return int(target)

    @staticmethod
    def sanitize_username(username: str) -> str:
        """Strips non-alphanumeric chars for API requests."""
        return re.sub(r'[^a-zA-Z0-9_]', '', username)

    @classmethod
    def validate_universe_id(cls, universe_id: Union[int, str]) -> int:
        try:
            val = int(universe_id)
            if val <= 0:
                raise ValueError
            return val
        except (ValueError, TypeError):
            raise ValueError(f"Invalid Universe ID: {universe_id}")

    @staticmethod
    def check_rate_limit_header(headers: dict) -> bool:
        """Inspects Roblox response headers for rate limit signals."""
        return 'Retry-After' in headers or headers.get('X-RateLimit-Limit') == '0'

def validate_payload(data: dict, required_keys: list):
    missing = [key for key in required_keys if key not in data]
    if missing:
        raise KeyError(f"Payload missing required Roblox fields: {', '.join(missing)}")
    return True