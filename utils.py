import functools
import logging

logger = logging.getLogger('roblox-utils')

class RobloxApiError(Exception):
    pass

def robust_request(retries=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_err = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_err = e
                    logger.warning(f'Attempt {attempt+1} failed: {e}')
            raise RobloxApiError(f'Failed after {retries} retries: {last_err}')
        return wrapper
    return decorator

def sanitize_robux(value):
    try:
        cleaned = int(str(value).replace(',', '').strip())
        return max(0, cleaned)
    except (ValueError, TypeError):
        return 0

def validate_game_id(game_id):
    if not isinstance(game_id, (int, str)):
        return None
    sid = str(game_id)
    return int(sid) if sid.isdigit() else None

if __name__ == '__main__':
    # Example usage
    val = sanitize_robux(' 1,000 ')
    print(f'Sanitized: {val}')