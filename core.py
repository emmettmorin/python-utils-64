import functools
import collections

class RobloxDataProcessor:
    """Cache-optimized interface for Roblox game data structures."""
    def __init__(self, capacity=1024):
        self.capacity = capacity
        self._cache = collections.OrderedDict()
        self._hits = 0

    def memoize_fetch(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in self._cache:
                self._hits += 1
                self._cache.move_to_end(key)
                return self._cache[key]
            
            result = func(*args, **kwargs)
            self._cache[key] = result
            self._cache.move_to_end(key)
            
            if len(self._cache) > self.capacity:
                self._cache.popitem(last=False)
            return result
        return wrapper

    def batch_process(self, data_list, transform_func):
        """Vectorized execution via list comprehension mapping."""
        return [transform_func(item) for item in data_list]

def optimize_roblox_payload(data):
    """Flatten nested game properties for faster serialization."""
    return {k: (v.id if hasattr(v, 'id') else v) for k, v in data.items()}