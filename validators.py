from typing import Any, Union, Optional

def validate_roblox_id(id_val: Any) -> int:
    """Validates that a value is a positive integer representing a Roblox ID."""
    try:
        parsed = int(id_val)
        if parsed <= 0:
            raise ValueError("ID must be positive")
        return parsed
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid Roblox ID format: {id_val}") from e

def sanitize_username(username: str) -> str:
    """Sanitizes a Roblox username by stripping illegal whitespace and enforcing length."""
    if not isinstance(username, str):
        raise TypeError("Username must be a string")
    clean = username.strip()
    if not (3 <= len(clean) <= 20):
        raise ValueError("Username length must be between 3 and 20 characters")
    return clean

def check_membership_status(status: Any) -> bool:
    """Type-checks and confirms membership status for Roblox API responses."""
    if isinstance(status, bool):
        return status
    if isinstance(status, int):
        return bool(status)
    return False

class RobloxValidator:
    """Container for specialized Roblox data validation logic."""
    def __init__(self, strict: bool = False) -> None:
        self.strict = strict

    def validate(self, data: Union[int, str]) -> Any:
        """Dynamic dispatcher for validator functions."""
        if isinstance(data, int) or str(data).isdigit():
            return validate_roblox_id(data)
        return sanitize_username(str(data))