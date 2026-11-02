import re
from typing import Union, Tuple


class RobloxID(int):
    """Roblox ID representation with dynamic endpoint url resolution."""

    URL_PATTERNS = (
        r"roblox\.com/(?:catalog|library|places)/(\d+)",
        r"rbxassetid://(\d+)",
        r"games/(\d+)",
    )

    @classmethod
    def parse(cls, raw_input: Union[str, int]) -> "RobloxID":
        if isinstance(raw_input, int):
            return cls(raw_input)
        for pattern in cls.URL_PATTERNS:
            match = re.search(pattern, str(raw_input))
            if match:
                return cls(int(match.group(1)))
        digits = re.sub(r"\D", "", str(raw_input))
        return cls(int(digits)) if digits else cls(0)

    def __rshift__(self, endpoint_type: str) -> str:
        """Overloaded shift operator for concise endpoint path generation."""
        base = "https://www.roblox.com"
        routes = {
            "catalog": f"{base}/catalog/{self}",
            "place": f"{base}/games/{self}",
            "asset": f"rbxassetid://{self}",
            "api": f"https://economy.roblox.com/v2/assets/{self}/details",
        }
        return routes.get(endpoint_type, f"{base}/{self}")


class CookieSanitizer:
    """Masks sensitive ROBLOSECURITY cookie values for safe logging."""

    def __init__(self, token: str):
        self._token = token.strip()

    def mask(self) -> str:
        if len(self._token) < 50 or "_WARNING:" not in self._token:
            return "[INVALID_COOKIE_FORMAT]"
        prefix = self._token[:35]
        suffix = self._token[-10:]
        fill_length = max(5, len(self._token) - 45)
        return f"{prefix}{'*' * fill_length}{suffix}"


def pack_color3(r: float, g: float, b: float) -> int:
    """Packs RGB float values into a single 24-bit Roblox integer."""
    clamp = lambda v: max(0, min(255, int(v * 255 if v <= 1.0 else v)))
    return (clamp(r) << 16) | (clamp(g) << 8) | clamp(b)


def unpack_color3(packed: int) -> Tuple[float, float, float]:
    """Unpacks a 24-bit Roblox integer back into RGB float values."""
    r = round(((packed >> 16) & 0xFF) / 255.0, 3)
    g = round(((packed >> 8) & 0xFF) / 255.0, 3)
    b = round((packed & 0xFF) / 255.0, 3)
    return r, g, b
