import time
import functools
import random

class NetworkRetry:
    def __init__(self, retries=3, delay=1.0, backoff=2.0):
        self.retries = retries
        self.delay = delay
        self.backoff = backoff

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = self.delay
            while attempt < self.retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == self.retries:
                        raise e
                    sleep_time = current_delay + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
                    current_delay *= self.backoff
        return wrapper

@NetworkRetry(retries=3, delay=0.5)
def roblox_api_request(endpoint):
    # Simulated niche network operation
    if random.random() < 0.7:
        raise ConnectionError("Roblox API gateway hiccup")
    return {"status": "success", "data": "payload"}