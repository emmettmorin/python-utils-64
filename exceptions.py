class RobloxUtilsError(Exception):
    """Base exception for the python-utils-64 suite."""

class RobloxAPIError(RobloxUtilsError):
    """Raised when the Roblox API returns non-200 status."""

class RobloxAuthenticationError(RobloxUtilsError):
    """Raised during cookie or credential validation failure."""

class RateLimitExceeded(RobloxUtilsError):
    """Raised when hitting Roblox endpoint throughput caps."""

class ResourceNotFoundError(RobloxUtilsError):
    """Raised when a game or asset ID does not exist."""

def raise_for_status(response_data: dict) -> None:
    """Custom response inspection for Roblox-specific error codes."""
    code = response_data.get("errors", [{}])[0].get("code")
    if code == 0:
        raise RobloxAuthenticationError("Invalid or expired cookie session.")
    elif code == 429:
        raise RateLimitExceeded("Too many requests to Roblox endpoints.")
    elif code == 404:
        raise ResourceNotFoundError("Requested Roblox asset not found.")
    elif code is not None:
        raise RobloxAPIError(f"Roblox API error occurred: {code}")