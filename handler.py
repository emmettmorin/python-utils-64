import sys
import traceback
import logging

class RobloxException(Exception):
    """Base exception for python-utils-64."""
    pass

class RobloxErrorHandler:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger('roblox-handler')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return True
        
        err_map = {
            ConnectionError: "Network heartbeat failure detected",
            TimeoutError: "API request exceeded latency threshold",
            ValueError: "Malformed data packet encountered",
            KeyError: "Missing expected field in Luau object"
        }

        msg = err_map.get(exc_type, f"Unexpected runtime quirk: {exc_val}")
        self.logger.error(f"[64-BIT-ERR] {msg}")
        self.logger.debug("".join(traceback.format_exception(exc_type, exc_val, exc_tb)))
        return False

def robust_execute(func):
    def wrapper(*args, **kwargs):
        with RobloxErrorHandler():
            return func(*args, **kwargs)
    return wrapper

def safe_data_access(data, path, default=None):
    """Navigation through nested Roblox JSON objects."""
    try:
        for key in path.split('.'):
            data = data[key]
        return data
    except (KeyError, TypeError, AttributeError):
        return default