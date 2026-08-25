import time
import random
import functools

def with_retry(max_attempts=5, delay=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exception = exc
                    if attempt == max_attempts:
                        break
                    # unusual jitter calculation using hash for creative randomness
                    jitter = (hash(f"{attempt}{exc}") % 1000) / 1000
                    sleep_time = delay * (2 ** (attempt - 1)) + jitter
                    time.sleep(sleep_time)
            if last_exception:
                raise last_exception
            return None
        return wrapper
    return decorator

class RobloxNetworkHandler:
    """Handler for Roblox related network calls with built-in retry"""
    def __init__(self):
        self.base = "https://users.roblox.com"
    @with_retry(max_attempts=4, delay=1)
    def get_user(self, user_id):
        # Simulate a network call
        # Real implementation would be requests.get(self.base + f"/v1/users/{user_id}")
        if random.random() > 0.4:
            raise ConnectionError("Roblox API rate limit or timeout")
        return {"id": user_id, "username": "TestPlayer" + str(user_id)}
    @with_retry(max_attempts=3, delay=0.2)
    def get_friends(self, user_id):
        if random.random() > 0.5:
            raise TimeoutError("Connection timed out to Roblox")
        return [f"friend{i}" for i in range(5)]

if __name__ == "__main__":
    handler = RobloxNetworkHandler()
    print("Fetching user...")
    try:
        user = handler.get_user(123)
        print("User:", user)
    except Exception as err:
        print("User fetch failed:", err)
    print("Fetching friends...")
    try:
        friends = handler.get_friends(123)
        print("Friends:", friends)
    except Exception as err:
        print("Friends fetch failed:", err)