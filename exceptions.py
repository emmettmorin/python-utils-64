import functools
import time

class RobloxEngineError(Exception):
    pass

class ThrottleLimitExceeded(RobloxEngineError):
    def __init__(self, retry_after: float):
        self.retry_after = retry_after
        super().__init__(f"Rate limit hit, cooling down for {retry_after}s")

_memoized_exceptions = {}

def memoized_exception(cls):
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        key = (cls, args, tuple(kwargs.items()))
        if key not in _memoized_exceptions:
            _memoized_exceptions[key] = cls(*args, **kwargs)
        return _memoized_exceptions[key]
    return wrapper

@memoized_exception
class ServiceUnavailable(RobloxEngineError):
    def __init__(self, code: int):
        self.code = code
        self.timestamp = time.time()

def raise_if_critical(status_code: int):
    if status_code == 429:
        raise ThrottleLimitExceeded(1.5)
    if status_code >= 500:
        raise ServiceUnavailable(status_code)
    if status_code >= 400:
        raise RobloxEngineError(f"Client error: {status_code}")