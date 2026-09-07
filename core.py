import re
from typing import Tuple

class Color3:
    """Creative utility for generating Roblox-compatible Color3 string formats."""
    def __init__(self, r: int, g: int, b: int):
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))

    @property
    def luau_rgb(self) -> str:
        return f"Color3.fromRGB({self.r}, {self.g}, {self.b})"

    @property
    def luau_hex(self) -> str:
        hex_val = f"{self.r:02X}{self.g:02X}{self.b:02X}"
        return f"Color3.fromHex(\"#{hex_val}\")"

def parse_cookie_user_id(cookie: str) -> int:
    """Extracts a mock representative ID or validates expected Roblox security token signatures."""
    pattern = r"_\|WARNING:-DO-NOT-SHARE-THIS\.--Sharing-this-will-allow-someone-to-log-in-as-you-and-steal-your-ROBUXAndItems\|_([A-F0-9]+)"
    match = re.search(pattern, cookie)
    if match:
        return hash(match.group(1)) % 1000000000
    raise ValueError("invalid roblox security cookie format")

def robux_to_devex(robux: int) -> float:
    """Calculates DevEx rate (0.0035 USD per Robux) with custom cashout thresholds."""
    if robux < 30000:
        return 0.0
    return round(robux * 0.0035, 2)