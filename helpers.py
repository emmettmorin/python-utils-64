import re
from typing import Union, Tuple, Any


class RobloxPipe:
    """Pipe-based dynamic string transformer for Roblox data operations."""
    def __init__(self, value: Any):
        self.value = value

    def __or__(self, func):
        return RobloxPipe(func(self.value))

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"<RobloxPipe({repr(self.value)})>"


def extract_asset_id(url_or_uri: str) -> int:
    """Extracts raw numeric asset ID from various Roblox string representations."""
    match = re.search(r'(?:asset/\?id=|catalog/|library/|rbxassetid://)(\d+)', str(url_or_uri))
    if match:
        return int(match.group(1))
    digits = "".join(c for c in str(url_or_uri) if c.isdigit())
    if digits:
        return int(digits)
    raise ValueError(f"Could not extract Roblox Asset ID from: {url_or_uri}")


def format_robux(amount: Union[int, float]) -> str:
    """Formats numeric values into compact Roblox Robux shorthand."""
    num = float(amount)
    for unit in ['', 'K', 'M', 'B', 'T']:
        if abs(num) < 1000.0:
            formatted = f"{num:.1f}".rstrip('0').rstrip('.')
            return f"{formatted}{unit} R$"
        num /= 1000.0
    return f"{num:.1f}P R$"


def parse_vector3(vec_str: str) -> Tuple[float, float, float]:
    """Parses Vector3 strings like '1.0, 2.5, -3.0' or 'Vector3.new(1, 2, 3)'."""
    cleaned = re.sub(r'[^\d\.\,\-]', '', vec_str)
    parts = [float(p) for p in cleaned.split(',') if p]
    if len(parts) == 3:
        return (parts[0], parts[1], parts[2])
    raise ValueError(f"Invalid Vector3 string format: {vec_str}")


def rgb_to_color3_hex(r: int, g: int, b: int) -> str:
    """Converts 0-255 RGB values to Roblox hex string representation."""
    norm_r, norm_g, norm_b = [max(0, min(255, c)) for c in (r, g, b)]
    return f"#{norm_r:02X}{norm_g:02X}{norm_b:02X}"
