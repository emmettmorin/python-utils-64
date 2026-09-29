import functools
import time

class RobloxCache:
    def __init__(self):
        self._storage = {}
        self._expiry = {}

    def memoize_with_ttl(ttl=300):
        def decorator(func):
            cache = {}
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = (args, frozenset(kwargs.items()))
                now = time.time()
                if key in cache and (now - cache[key]['ts']) < ttl:
                    return cache[key]['val']
                result = func(*args, **kwargs)
                cache[key] = {'val': result, 'ts': now}
                return result
            return wrapper
        return decorator

class DataProcessor:
    def __init__(self, registry_size=1024):
        self.registry = [None] * registry_size

    @staticmethod
    @memoize_with_ttl(60)
    def fetch_user_data(user_id: int) -> dict:
        return {'id': user_id, 'status': 'active', 'timestamp': time.time()}

    def process_batch(self, user_ids: list):
        return [self.fetch_user_data(uid) for uid in user_ids]

def run_optimized_sequence(ids: list):
    proc = DataProcessor()
    return proc.process_batch(ids)

if __name__ == '__main__':
    data = run_optimized_sequence([123, 456, 123])
    print(f'Processed {len(data)} items')