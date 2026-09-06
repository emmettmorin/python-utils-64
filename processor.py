import re
import urllib.request
import json
from typing import Dict, Any, Generator

class RobloxAssetProcessor:
    """Creative processor for Roblox asset resolution and security masking."""
    
    # Regex for various Roblox asset formats
    ASSET_PATTERN = re.compile(r"(?:rbxassetid://|/asset/\?id=|roblox\.com/catalog/)(\d+)")

    def __init__(self, cookie: str = None):
        self._cookie = cookie

    @property
    def masked_cookie(self) -> str:
        """Masks the sensitive .ROBLOSECURITY token for safe logging."""
        if not self._cookie:
            return ""
        parts = self._cookie.split("_|WARNINGExternal-")
        target = parts[-1] if parts else self._cookie
        return f"WarningMasked...{target[-20:] if len(target) > 20 else '...'}"

    def extract_asset_ids(self, text: str) -> Generator[int, None, None]:
        """Extracts all Roblox asset IDs found within a string or script source."""
        for match in self.ASSET_PATTERN.finditer(text):
            yield int(match.group(1))

    def fetch_universe_info(self, place_id: int) -> Dict[str, Any]:
        """Retrieves universe information for a given Place ID using Roblox API."""
        url = f"https://apis.roblox.com/universes/v1/places/{place_id}/universe"
        headers = {"User-Agent": "RobloxUtils64/1.0"}
        if self._cookie:
            headers["Cookie"] = f".ROBLOSECURITY={self._cookie}"
            
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            return {"error": str(e), "placeId": place_id, "universeId": None}

    def compile_manifest(self, source_code: str) -> Dict[int, Dict[str, Any]]:
        """Processes source code, extracts asset IDs, and maps them to dynamic configurations."""
        return {
            asset_id: {
                "resolved_url": f"https://assetdelivery.roblox.com/v1/asset/?id={asset_id}",
                "cdn_link": f"rbxassetid://{asset_id}",
                "processed_status": "resolved"
            }
            for asset_id in self.extract_asset_ids(source_code)
        }