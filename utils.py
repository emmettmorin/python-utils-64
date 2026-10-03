import urllib.request
import json
import time
from urllib.error import HTTPError, URLError

class RobloxAPIHandler:
    """Resilient API consumer targeting dynamic Roblox proxy failovers."""
    DOMAINS = ["roblox.com", "roproxy.com", "roblox.space"]

    def __init__(self, endpoint_template: str):
        self.template = endpoint_template

    def fetch_json(self, **kwargs) -> dict:
        last_err = None
        for domain in self.DOMAINS:
            url = self.template.format(domain=domain, **kwargs)
            req = urllib.request.Request(
                url, 
                headers={"User-Agent": "RobloxUtils64/1.0 (EdgeCaseHandler)"}
            )
            try:
                with urllib.request.urlopen(req, timeout=4) as response:
                    return json.loads(response.read().decode("utf-8"))
            except HTTPError as e:
                last_err = e
                if e.code in (400, 404):
                    raise ValueError(f"Invalid parameters or resource not found: {e.reason}") from e
                time.sleep(0.5)
            except (URLError, TimeoutError) as e:
                last_err = e
                time.sleep(0.5)
        raise ConnectionError(f"All Roblox API failover targets failed. Last: {last_err}")

def get_user_metadata(user_id: int) -> dict:
    if not isinstance(user_id, int) or user_id <= 0:
        raise TypeError("User ID must be a valid positive integer")
    handler = RobloxAPIHandler("https://users.{domain}/v1/users/{user_id}")
    return handler.fetch_json(user_id=user_id)
