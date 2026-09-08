class RobloxError(Exception):
    """Base exception for all roblox-related operation failures."""

def safe_execute(func):
    """Decorator for graceful failure in non-critical roblox pipeline calls."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ConnectionError, TimeoutError) as e:
            return {'status': 'retryable_fail', 'reason': str(e)}
        except ValueError as e:
            return {'status': 'malformed_data', 'reason': str(e)}
        except Exception as e:
            return {'status': 'catastrophic_failure', 'reason': 'unhandled_void'}
    return wrapper

class RobloxRateLimit(RobloxError):
    """Thrown when the api hits too many requests."""

def validate_roblox_id(id_val):
    """Ensure the roblox id is a non-negative integer."""
    if not isinstance(id_val, int) or id_val < 0:
        raise RobloxError(f'Invalid roblox resource identifier: {id_val}')
    return True

class StateManager:
    """Container for stateful edge case recovery operations."""
    def __init__(self):
        self.cache = {}

    def fetch_safe(self, key, fallback=None):
        return self.cache.get(key, fallback)