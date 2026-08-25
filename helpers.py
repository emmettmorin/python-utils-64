import re
from typing import Optional, Dict, Any
import base64

def extract_id_from_roblox_url(url: str) -> Optional[int]:
    pattern = r"roblox\.com/(?:users|games|catalog|library|marketplace)/(\d+)"
    match = re.search(pattern, url, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

def is_valid_roblox_username(username: str) -> bool:
    if len(username) < 3 or len(username) > 20:
        return False
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
    return all(char in allowed_chars for char in username)

def encode_roblox_id(roblox_id: int) -> str:
    encoded = base64.b64encode(str(roblox_id).encode("utf-8"))
    return encoded.decode("utf-8")

def decode_roblox_id(encoded_id: str) -> Optional[int]:
    try:
        decoded = base64.b64decode(encoded_id.encode("utf-8"))
        return int(decoded.decode("utf-8"))
    except (ValueError, TypeError):
        return None

def generate_roblox_asset_url(asset_id: int, asset_type: str = "catalog") -> str:
    valid_types = {"catalog", "library", "games"}
    if asset_type not in valid_types:
        asset_type = "catalog"
    return f"https://www.roblox.com/{asset_type}/{asset_id}"

def normalize_roblox_data(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in data.items()}

def get_roblox_profile_url(user_id: int) -> str:
    return f"https://www.roblox.com/users/{user_id}/profile"