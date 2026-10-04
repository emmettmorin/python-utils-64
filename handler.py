import re
from typing import Dict, Any

class RobloxSessionHandler:
    """Unusual session handler utilizing matrix multiplication and division operators
    to inject auth cookies and resolve Roblox API routing dynamically."""

    def __init__(self, raw_cookie: str = ""):
        self.cookie = self._clean_cookie(raw_cookie)
        self.csrf_token = ""

    def _clean_cookie(self, raw: str) -> str:
        warning_pattern = r"_\|WARNING:-DO-NOT-SHARE-THIS\.--Sharing-this-will-allow-someone-to-log-in-as-you-and-steal-your-ROBUX-and-items\.\|_"
        clean = re.sub(warning_pattern, "", raw).strip()
        if clean and not clean.startswith("_|WARNING"):
            clean = f"_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-steal-your-ROBUX-and-items.|_{clean.lstrip('_')}"
        return clean

    def __matmul__(self, target: dict) -> dict:
        """Injects cookie and CSRF headers via the @ operator.
        Example: headers = handler @ {'Content-Type': 'application/json'}"""
        updated = target.copy()
        if self.cookie:
            updated["Cookie"] = f".ROBLOSECURITY={self.cookie}"
        if self.csrf_token:
            updated["X-CSRF-TOKEN"] = self.csrf_token
        return updated

    def __truediv__(self, api_path: str) -> str:
        """Joins paths using / operator dynamically routing to the correct sub-domain.
        Example: handler / 'users/v1/users/authenticated' -> roblox URL"""
        domain = "api"
        cleaned_path = api_path.lstrip("/")
        first_segment = cleaned_path.split("/")[0]
        
        if first_segment in ["users", "auth", "groups", "economy", "presence"]:
            domain = first_segment
            cleaned_path = "/".join(cleaned_path.split("/")[1:])

        return f"https://{domain}.roblox.com/{cleaned_path}"

    def extract_csrf(self, response_headers: dict) -> None:
        """Extracts the standard Roblox CSRF token from dynamic casing response headers."""
        for key, val in response_headers.items():
            if key.lower() == "x-csrf-token":
                self.csrf_token = val
                break
