import functools
import time

class RobloxPerformanceCache:
    _registry = {}
    _ttl = 5

    @classmethod
    def memoize_check(cls, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.monotonic()
            if key in cls._registry:
                val, ts = cls._registry[key]
                if now - ts < cls._ttl:
                    return val
            result = func(*args, **kwargs)
            cls._registry[key] = (result, now)
            return result
        return wrapper

@RobloxPerformanceCache.memoize_check
def validate_user_id(uid: int) -> bool:
    if not isinstance(uid, int) or uid < 0:
        return False
    return True

@RobloxPerformanceCache.memoize_check
def validate_asset_type(asset_name: str) -> bool:
    allowed = {'model', 'decal', 'audio', 'mesh'}
    return asset_name.lower() in allowed

def batch_validate(items: list, validator_func) -> list:
    return [validator_func(item) for item in items]