import functools
import logging

class RobloxApiError(Exception):
    pass

def robust_request(retries=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_ex = e
                    logging.warning(f"Attempt {attempt+1} failed for {func.__name__}")
            raise RobloxApiError(f"Failed after {retries} attempts: {last_ex}")
        return wrapper
    return decorator

def parse_roblox_id(value):
    try:
        uid = int(value)
        if uid < 0:
            raise ValueError("Negative ID")
        return uid
    except (ValueError, TypeError):
        logging.error(f"Invalid Roblox ID format: {value}")
        return None

def safe_execute(callback, fallback=None):
    try:
        return callback()
    except Exception as err:
        logging.critical(f"Execution trapped: {err}")
        return fallback

logging.basicConfig(level=logging.INFO)