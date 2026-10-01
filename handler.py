import functools
import time

class RobloxDataHandler:
    """
    High-performance caching layer for Roblox API endpoints.
    Uses slot-based storage and a TTL-managed lookup table.
    """
    __slots__ = ('_cache', '_ttl', '_expiry')

    def __init__(self, ttl=30):
        self._cache = {}
        self._ttl = ttl
        self._expiry = {}

    def memoize_roblox_request(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.time()
            
            if key in self._cache and now < self._expiry[key]:
                return self._cache[key]
            
            result = func(*args, **kwargs)
            self._cache[key] = result
            self._expiry[key] = now + self._ttl
            return result
        return wrapper

    def batch_process(self, items, func):
        # Vectorized-style operation for bulk object processing
        return [func(item) for item in items]

    def purge_stale(self):
        now = time.time()
        keys_to_delete = [k for k, v in self._expiry.items() if now > v]
        for k in keys_to_delete:
            del self._cache[k]
            del self._expiry[k]

instance = RobloxDataHandler()