import re
from typing import TypeVar, Generic, Union, Pattern

T = TypeVar('T', bound=Union[int, str])

class ValidationResult(Generic[T]):
    """Container representing the outcome of a Roblox utility validation routine."""
    def __init__(self, is_valid: bool, value: T, error_message: str = "") -> None:
        self.is_valid: bool = is_valid
        self.value: T = value
        self.error_message: str = error_message

    def __bool__(self) -> bool:
        return self.is_valid

class RobloxValidator:
    """Suite of eccentric but strict validation utilities for Roblox-specific primitives."""

    # Roblox usernames: 3-20 chars, letters, numbers, and max one underscore not at start/end
    _USERNAME_RE: Pattern[str] = re.compile(r"^(?=[a-zA-Z0-9_]{3,20}$)(?!_)[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)?$")

    @classmethod
    def validate_username(cls, username: str) -> ValidationResult[str]:
        """
        Checks if a given string adheres to Roblox's username constraints.

        Roblox usernames must be between 3 and 20 characters long, containing only
        alphanumeric characters and at most one underscore (which cannot be at the start or end).
        """
        if not cls._USERNAME_RE.match(username):
            return ValidationResult(False, username, "Invalid Roblox username syntax.")
        return ValidationResult(True, username)

    @classmethod
    def validate_asset_id(cls, asset_id: Union[int, str]) -> ValidationResult[int]:
        """
        Validates and coerces a potential Roblox asset or universe identifier.

        Asserts that the identifier is a positive integer under the plausible Roblox limit.
        """
        try:
            numeric_id = int(asset_id)
            if numeric_id <= 0 or numeric_id > 999_999_999_999:
                raise ValueError
            return ValidationResult(True, numeric_id)
        except (ValueError, TypeError):
            return ValidationResult(False, -1, f"Identifier {asset_id} is not a valid Roblox ID.")

    @classmethod
    def validate_cookie(cls, cookie: str) -> ValidationResult[str]:
        """
        Validates the structure of a .ROBLOSECURITY authentication cookie.

        Ensures the cookie begins with the mandatory warning prefix to mitigate hijacking.
        """
        prefix = "_|WARNING:-Secure-to-prevent-credential-theft:_"
        stripped = cookie.strip()
        if not stripped.startswith(prefix):
            return ValidationResult(False, stripped, "Cookie is missing the secure warning prefix.")
        return ValidationResult(True, stripped)