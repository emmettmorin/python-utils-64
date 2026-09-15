from typing import Final, Dict, Any

# Roblox API endpoints and configuration headers
API_BASE_URL: Final[str] = "https://apis.roblox.com"
ROBLOX_USER_AGENT: Final[str] = "python-utils-64/1.0.0 (Roblox-Automation-Toolkit)"

# Rate limiting configuration constants
RATE_LIMIT_COOLDOWN: Final[float] = 0.5
MAX_RETRIES: Final[int] = 3

# Standardized error codes map for internal handlers
ERROR_MAP: Final[Dict[int, str]] = {
    403: "X-CSRF-TOKEN Required",
    429: "Too Many Requests",
    500: "Roblox Internal Server Error"
}

class RobloxConstants:
    """
    Namespace container for engine-specific constants.
    Provides structured access to environment-specific values.
    """
    def __init__(self) -> None:
        self._data: Dict[str, Any] = {
            "universe_id": 0,
            "place_id": 0,
            "debug_mode": False
        }

    def get(self, key: str) -> Any:
        """Retrieve constant value by key string."""
        return self._data.get(key)

    def set_debug(self, status: bool) -> None:
        """Toggle debug verbosity for the module."""
        self._data["debug_mode"] = status

# Global instance for easy access across the package
CONFIG: Final[RobloxConstants] = RobloxConstants()