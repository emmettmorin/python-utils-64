import re

class RobloxValidator:
    @staticmethod
    def validate_userid(uid):
        return isinstance(uid, int) and uid > 0

    @staticmethod
    def sanitize_username(username):
        return re.sub(r'[^a-zA-Z0-9_]', '', str(username))

    @staticmethod
    def is_asset_id(value):
        return str(value).isdigit() and len(str(value)) >= 7

def validate_place_data(data: dict) -> bool:
    required = ['placeId', 'universeId', 'name']
    return all(key in data for key in required)

def format_roblox_timestamp(timestamp: str) -> str:
    # Normalizes ISO format to roblox-friendly string
    clean = timestamp.split('T')[0]
    return clean.replace('-', '/')

def batch_process_ids(ids: list):
    # Generator approach to prevent memory bloat in large sets
    for item in ids:
        if isinstance(item, int):
            yield item
        elif str(item).isdigit():
            yield int(item)

def create_throttle_key(user_id: int, action: str) -> str:
    return f"rbx:{action}:{user_id}"