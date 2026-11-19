import typing

def validate_roblox_input(data: typing.Any) -> bool:
    """Sanity check for raw Roblox API payloads."""
    if not isinstance(data, dict):
        return False
    
    required = {"userId", "placeId", "gameId"}
    if not required.issubset(data.keys()):
        return False

    # Roblox IDs are typically positive integers
    for key in required:
        val = data[key]
        if not isinstance(val, int) or val <= 0:
            return False
    return True

def sanitize_payload(payload: dict) -> dict:
    """Strip non-essential metadata from incoming game packets."""
    return {k: v for k, v in payload.items() if k in {"userId", "placeId", "gameId", "timestamp"}}

class RobloxInputError(Exception):
    """Custom exception for invalid engine communications."""
    pass

def process_securely(data: typing.Any):
    if not validate_roblox_input(data):
        raise RobloxInputError("Malformed packet structure detected")
    return sanitize_payload(data)