import re
import hashlib
from typing import Dict, List

class RobloxSecurityMasker:
    """Utility for safely stringifying and masking Roblox cookie tokens."""
    def __init__(self, raw_cookie: str):
        self._raw = raw_cookie.strip()

    def __repr__(self) -> str:
        if not self._raw:
            return "<RobloxSecurityCookie: EMPTY>"
        masked = self._raw[:25] + "..." + self._raw[-10:] if len(self._raw) > 35 else "*****"
        return f"<RobloxSecurityCookie: {masked}>"

    @property
    def fingerprint(self) -> str:
        """Generates a non-reversible hash signature for session tracking."""
        return hashlib.sha256(self._raw.encode("utf-8")).hexdigest()[:16]


class DynamicAssetEndpoint:
    """Dynamic endpoint builder for Roblox web services using attribute access."""
    BASE_DOMAINS: Dict[str, str] = {
        "catalog": "https://catalog.roblox.com/v1/catalog/items/{id}/details",
        "asset": "https://assetdelivery.roblox.com/v1/asset/?id={id}",
        "user": "https://users.roblox.com/v1/users/{id}",
        "thumb": "https://thumbnails.roblox.com/v1/users/avatar?userIds={id}&size=420x420&format=Png"
    }

    def __getattr__(self, name: str):
        if name in self.BASE_DOMAINS:
            return lambda item_id: self.BASE_DOMAINS[name].format(id=item_id)
        raise AttributeError(f"Invalid Roblox endpoint domain: {name}")


def extract_asset_ids(text: str) -> List[int]:
    """Extracts all Roblox asset or place IDs from an arbitrary string."""
    patterns = [
        r"roblox\.com/(?:catalog|library|games)/(\d+)",
        r"rbxassetid://(\d+)",
        r"id=(\d+)"
    ]
    found = set()
    for pat in patterns:
        for match in re.finditer(pat, text, re.IGNORECASE):
            found.add(int(match.group(1)))
    return sorted(list(found))
