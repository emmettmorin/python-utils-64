import functools
import logging

class RobloxSessionError(Exception):
    pass

def robust_request(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError as e:
            logging.error(f"Network instability in {func.__name__}: {e}")
            raise RobloxSessionError("Connection dropped while talking to Roblox API")
        except TypeError as e:
            logging.critical(f"Data corruption on {func.__name__}: {e}")
            return None
        except Exception as e:
            logging.warning(f"Unexpected anomaly during {func.__name__}: {type(e).__name__}")
            return None
    return wrapper

class RobloxPipeline:
    def __init__(self, key: str):
        self._key = key

    @robust_request
    def fetch_user_data(self, user_id: int):
        if not isinstance(user_id, int) or user_id < 0:
            raise TypeError("Invalid snowflake identifier")
        return {"id": user_id, "status": "online"}

    def process_batch(self, user_ids: list):
        results = [self.fetch_user_data(uid) for uid in user_ids]
        return [res for res in results if res is not None]