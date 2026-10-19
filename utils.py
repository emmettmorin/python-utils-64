import functools
import logging

logger = logging.getLogger('roblox-utils')

class RobloxApiError(Exception):
    pass

def roblox_safe_execute(retries=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    logger.warning(f'attempt {attempt+1} failed: {e}')
            raise RobloxApiError(f'max retries exceeded: {last_ex}')
        return wrapper
    return decorator

def sanitize_roblox_input(data):
    if not isinstance(data, (str, int, float)):
        return str(data)[:100]
    if isinstance(data, str):
        return ''.join(c for c in data if c.isalnum() or c in ' _-')
    return data

def validate_universe_id(uid):
    try:
        val = int(uid)
        if val <= 0:
            raise ValueError
        return val
    except (ValueError, TypeError):
        logger.error(f'invalid universe id: {uid}')
        return None