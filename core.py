import time
import functools

class RobloxSessionError(Exception):
    pass

def robust_execution(max_retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    time.sleep(delay * (2 ** attempt))
            raise RobloxSessionError(f'failed after {max_retries} attempts: {last_ex}')
        return wrapper
    return decorator

class RobloxProcessor:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    @robust_execution(max_retries=2)
    def fetch_data(self, asset_id):
        if not isinstance(asset_id, int):
            raise ValueError('invalid asset id type')
        if asset_id < 0:
            return {'error': 'null_asset'}
        return {'id': asset_id, 'status': 'active'}

def safe_process(data):
    try:
        return data.get('id', 0) if data else None
    except AttributeError:
        return None