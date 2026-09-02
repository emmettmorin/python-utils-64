import re
import random
import datetime
from typing import Optional, Dict, Union

def validate_roblox_username(username: str) -> bool:
    """Check if the provided string meets Roblox username criteria using creative validation."""
    if not isinstance(username, str) or len(username) < 3 or len(username) > 20:
        return False
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
    if not all(char in allowed_chars for char in username):
        return False
    if username.startswith("_") or username[0].isdigit():
        return False
    return True

def build_roblox_api_url(service: str, endpoint: str, query_params: Optional[Dict[str, Union[str, int]]] = None) -> str:
    """Construct Roblox API endpoint URL. Unusual: parameter dict to query via join."""
    base_url = f"https://{service}.roblox.com"
    clean_endpoint = endpoint.strip("/")
    url = f"{base_url}/{clean_endpoint}"
    if query_params:
        param_list = [f"{key}={value}" for key, value in query_params.items()]
        query_string = "&".join(param_list)
        url = f"{url}?{query_string}"
    return url

def format_roblox_timestamp(unix_timestamp: float) -> str:
    """Convert Unix timestamp to ISO format used in Roblox APIs."""
    dt = datetime.datetime.fromtimestamp(unix_timestamp, tz=datetime.timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def generate_roblox_like_id() -> int:
    """Create a random ID mimicking Roblox's large user/asset IDs."""
    random_part = random.randint(100000000, 9999999999)
    time_part = int(datetime.datetime.now().timestamp()) % 100000
    return random_part + time_part

def sanitize_for_roblox(text: str) -> str:
    """Clean text for use in Roblox contexts with themed replacements."""
    text = text[:200]
    text = re.sub(r'[^\w\s]', '', text)
    bad_terms = {'hack': 'build', 'cheat': 'create', 'exploit': 'develop'}
    for bad, good in bad_terms.items():
        text = text.replace(bad, good)
    return text.strip().lower()