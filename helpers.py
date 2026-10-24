import re
from typing import Union, Dict, Any, Callable, List

class RobloxShorthand:
    """Creative conversion pipeline for Roblox currency and entity IDs."""
    
    _UNITS = [(1_000_000_000, 'B'), (1_000_000, 'M'), (1_000, 'K')]
    
    @classmethod
    def format_robux(cls, amount: Union[int, float]) -> str:
        """Formats raw integer Robux into compact visual notation (e.g. R$ 1.5M)."""
        num = float(amount)
        if num < 0:
            return f"-R$ {cls.format_robux(abs(num))[3:]}"
        for threshold, suffix in cls._UNITS:
            if num >= threshold:
                val = round(num / threshold, 1)
                formatted = f"{val:.1f}".rstrip('0').rstrip('.')
                return f"R$ {formatted}{suffix}"
        return f"R$ {int(num)}"

def parse_roblox_id(input_val: Union[str, int]) -> int:
    """Extracts a valid 64-bit integer Roblox ID from URLs or raw strings."""
    if isinstance(input_val, int):
        return input_val
    
    match = re.search(r'(?:catalog|library|games|users|assets|groups)/(\d+)', str(input_val))
    if match:
        return int(match.group(1))
    
    digits = ''.join(filter(str.isdigit, str(input_val)))
    if digits:
        return int(digits)
    
    raise ValueError(f"Could not resolve Roblox ID from source: {input_val}")

def make_asset_uri(asset_id: Union[str, int], cdn_type: str = "asset") -> str:
    """Generates standard rbxassetid or HTTP content endpoints via lookup table."""
    clean_id = parse_roblox_id(asset_id)
    endpoints = {
        "asset": f"rbxassetid://{clean_id}",
        "cdn": f"https://assetdelivery.roblox.com/v1/asset/?id={clean_id}",
        "avatar": f"https://www.roblox.com/headshot-thumbnail/image?userId={clean_id}&width=420&height=420&format=png",
        "gamepass": f"https://www.roblox.com/game-pass/{clean_id}"
    }
    return endpoints.get(cdn_type.lower(), f"rbxassetid://{clean_id}")

def batch_process_ids(raw_items: List[Any], transformer: Callable[[int], Any] = lambda x: x) -> Dict[int, Any]:
    """Helper using dict comprehensions to deduplicate and transform Roblox IDs."""
    results = {}
    for item in raw_items:
        try:
            rid = parse_roblox_id(item)
            results[rid] = transformer(rid)
        except ValueError:
            continue
    return results
