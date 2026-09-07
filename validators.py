import time
import functools
import random

def retry_request(max_retries=3, base_delay=1.0, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = base_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == max_retries - 1:
                        break
                    time.sleep(current_delay + random.uniform(0, 0.1))
                    current_delay *= backoff
            raise last_exception
        return wrapper
    return decorator

def validate_roblox_response(response):
    if response is None:
        return False
    if hasattr(response, 'status_code'):
        return 200 <= response.status_code < 300
    return isinstance(response, dict) and 'success' in response and response['success'] is True

class RobloxNetworkValidator:
    @staticmethod
    def is_valid_payload(data):
        required_fields = ['universeId', 'placeId']
        return all(field in data for field in required_fields)