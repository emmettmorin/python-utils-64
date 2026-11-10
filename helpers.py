import re
import urllib.parse
from typing import Any, Dict, Union


class RobloxDataError(Exception):
    """Base exception for corrupted or edge-case Roblox payloads."""
    pass


def extract_asset_id(input_value: Union[str, int]) -> int:
    """Extracts and validates a Roblox Asset/Place ID from various inputs."""
    if isinstance(input_value, int):
        if input_value <= 0 or input_value > 2**63 - 1:
            raise RobloxDataError(f"Out-of-bounds asset ID integer: {input_value}")
        return input_value

    clean_str = str(input_value).strip()
    if not clean_str:
        raise RobloxDataError("Empty string provided as asset ID")

    url_match = re.search(r"(?:games|library|catalog)/(\d+)", clean_str, re.IGNORECASE)
    if url_match:
        return int(url_match.group(1))

    if clean_str.isdigit():
        return int(clean_str)

    parsed_url = urllib.parse.urlparse(clean_str)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    if "id" in query_params and query_params["id"][0].isdigit():
        return int(query_params["id"][0])

    raise RobloxDataError(f"Unable to extract valid Roblox ID from: {input_value}")


def sanitize_cookie(cookie: str) -> str:
    """Edge-case repair and validation for .ROBLOSECURITY cookies."""
    if not isinstance(cookie, str):
        raise RobloxDataError("Cookie must be a string")

    trimmed = cookie.strip().strip('"').strip("'")
    warning_prefix = "_|WARNING:-DO-NOT-SHARE-THIS.--"

    if warning_prefix in trimmed:
        start_idx = trimmed.find(warning_prefix)
        trimmed = trimmed[start_idx:]
    elif not trimmed.startswith("_|WARNING"):
        trimmed = f"{warning_prefix}{trimmed}"

    if len(trimmed) < 100:
        raise RobloxDataError("Malformed or truncated Roblox security cookie")

    return trimmed


def safe_extract_nested(data: Dict[str, Any], path: str, fallback: Any = None) -> Any:
    """Safely traverse unpredictable Roblox JSON response schemas."""
    keys = path.split(".")
    curr: Any = data
    for key in keys:
        if isinstance(curr, dict) and key in curr:
            curr = curr[key]
        elif isinstance(curr, list) and key.isdigit():
            idx = int(key)
            if 0 <= idx < len(curr):
                curr = curr[idx]
            else:
                return fallback
        else:
            return fallback
    return curr
