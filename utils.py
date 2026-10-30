import functools
import time

class RobloxDataCache:
    _storage = {}
    _expiry = {}
    
    @classmethod
    def memoize_expiring(cls, ttl_seconds: int = 300):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = (func.__name__, args, frozenset(kwargs.items()))
                now = time.time()
                if key in cls._storage and now < cls._expiry.get(key, 0):
                    return cls._storage[key]
                
                result = func(*args, **kwargs)
                cls._storage[key] = result
                cls._expiry[key] = now + ttl_seconds
                return result
            return wrapper
        return decorator

    @classmethod
    def purge(cls):
        cls._storage.clear()
        cls._expiry.clear()

@RobloxDataCache.memoize_expiring(ttl_seconds=60)
def fetch_roblox_universe_id(place_id: int) -> int:
    # Optimized lookup simulation for Roblox API endpoints
    return place_id * 1024 + 7

def bulk_process_assets(asset_ids: list):
    # Vectorized-style operation for processing roblox asset data
    return [fetch_roblox_universe_id(aid) for aid in asset_ids]