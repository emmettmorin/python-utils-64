import time
import functools

def roblox_safe_throttle(rate_limit: float):
    def decorator(func):
        last_called = [0.0]
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < rate_limit:
                time.sleep(rate_limit - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

def parse_roblox_id(input_val: any) -> int:
    try:
        if isinstance(input_val, str):
            return int(''.join(filter(str.isdigit, input_val)))
        return int(input_val)
    except (ValueError, TypeError):
        return 0

def format_asset_url(asset_id: int, base: str = "rbxassetid://") -> str:
    return f"{base}{asset_id}"

def batch_process(items: list, chunk_size: int = 100):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

def retry_request(attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == attempts - 1: raise
                    time.sleep(delay * (2 ** i))
        return wrapper
    return decorator