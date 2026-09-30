class RobloxUtilsError(Exception):
    """Base exception for python-utils-64."""

class DataModelSyncError(RobloxUtilsError):
    """Raised when synchronization with Roblox DataModel fails."""

class APIProtocolViolation(RobloxUtilsError):
    """Raised when interacting with unsupported endpoints."""

class PayloadCorruptionError(RobloxUtilsError):
    def __init__(self, message, raw_payload=None):
        super().__init__(message)
        self.raw_payload = raw_payload

def raise_if_nil(value, message="Nil reference encountered"):
    if value is None:
        raise RobloxUtilsError(message)

class ExceptionFormatter:
    @staticmethod
    def format_as_roblox_log(exc: Exception) -> str:
        return f"[ROBLOX-UTILS-64][ERROR]: {type(exc).__name__} -> {str(exc)}"

__all__ = [
    'RobloxUtilsError', 
    'DataModelSyncError', 
    'APIProtocolViolation', 
    'PayloadCorruptionError', 
    'raise_if_nil', 
    'ExceptionFormatter'
]