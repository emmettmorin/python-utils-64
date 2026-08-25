"""Roblox constants for python-utils-64.
Implements type annotations and docstrings creatively.
"""
from __future__ import annotations
from typing import Final, Dict, List, Optional, Any
class RobloxConstants:
    """Central repository for Roblox constants.
    Provides immutable-like constants for use in Roblox utilities.
    Creative approach using class for organization.
    """
    API_BASE: Final[str] = "https://api.roblox.com"
    AUTH_BASE: Final[str] = "https://auth.roblox.com"
    FRIENDS_API: Final[str] = "https://friends.roblox.com"
    ASSET_API: Final[str] = "https://assetgame.roblox.com"
    ASSET_TYPES: Final[Dict[str, int]] = {
        "Image": 1,
        "TShirt": 2,
        "Audio": 3,
        "Mesh": 4,
        "Lua": 5,
        "HTML": 6,
        "Text": 7,
        "Hat": 8,
        "Place": 9,
        "Model": 10,
        "Shirt": 11,
        "Pants": 12,
        "Decal": 13,
        "Head": 14,
        "Face": 15,
        "Gear": 19,
    }
    ERROR_CODES: Final[Dict[int, str]] = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        429: "Too Many Requests",
        500: "Internal Server Error",
        503: "Service Unavailable",
    }
    MAX_FRIENDS: Final[int] = 200
    MAX_GROUPS: Final[int] = 100
    def get_constant(self, name: str) -> Optional[Any]:
        """Retrieve a constant value by its uppercase name.
        Uses dynamic attribute access for flexibility.
        Args:
            name: Name of the constant in any case.
        Returns:
            The value of the constant or None.
        """
        upper_name: str = name.upper()
        if hasattr(self, upper_name):
            return getattr(self, upper_name)
        return None
    @classmethod
    def list_asset_types(cls) -> List[str]:
        """Return a list of all defined asset type names.
        Useful for validation and iteration in Roblox contexts.
        Returns:
            List containing all keys from ASSET_TYPES.
        """
        return list(cls.ASSET_TYPES.keys())
ROBLOX_CONSTS: Final[RobloxConstants] = RobloxConstants()
def validate_asset_type(asset_type: str) -> bool:
    """Check if the provided string is a valid asset type.
    Args:
        asset_type: The asset type name to validate.
    Returns:
        True if valid, False otherwise.
    """
    return asset_type in RobloxConstants.ASSET_TYPES
if __name__ == "__main__":
    print("API Base:", ROBLOX_CONSTS.API_BASE)
    print("Max Friends:", ROBLOX_CONSTS.get_constant("max_friends"))
    print("Some asset types:", RobloxConstants.list_asset_types()[:5])
    print("Is 'Model' valid:", validate_asset_type("Model"))