import time
import functools
import random

def retry_network_op(max_attempts=3, delay=1.0, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    time.sleep(current_delay + random.uniform(0, 0.1))
                    current_delay *= backoff
        return wrapper
    return decorator

@retry_network_op(max_attempts=3, delay=0.5)
def fetch_roblox_data(url):
    # Simulate volatile network state for roblox api
    if random.random() < 0.7:
        raise ConnectionError("roblox endpoint throttle encountered")
    return {"status": "success", "data": "bloxy_payload"}

if __name__ == "__main__":
    try:
        result = fetch_roblox_data("https://api.roblox.com/v1/user")
        print(result)
    except Exception as err:
        print(f"critical failure after retries: {err}")