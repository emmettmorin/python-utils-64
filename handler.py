import json
import re
from typing import Any, Dict, Union

class RobloxAPIEdgeError(Exception):
    """Base exception for Roblox API anomalous responses."""
    pass

class RateLimitExceeded(RobloxAPIEdgeError):
    def __init__(self, retry_after: int = 60):
        self.retry_after = retry_after
        super().__init__(f"Rate limited. Cool down for {retry_after}s")

class RobloxEdgeCaseHandler:
    """Resilient parser recovering from weird Roblox API edge cases."""

    @staticmethod
    def sanitize_id(identifier: Union[int, str, float]) -> int:
        """Coerces string/float/corrupted inputs into positive Roblox ID."""
        try:
            cleaned = re.sub(r'[^\d-]', '', str(identifier))
            val = int(float(cleaned))
            if val <= 0:
                raise ValueError("Roblox IDs must be strictly positive")
            return val
        except (ValueError, TypeError) as err:
            raise RobloxAPIEdgeError(f"Malformed Roblox ID '{identifier}': {err}")

    @staticmethod
    def parse_response_safe(raw_data: Union[str, bytes, dict], default_key: str = "data") -> Dict[str, Any]:
        """Handles HTML error pages, XML leaks, or broken JSON payloads."""
        if isinstance(raw_data, dict):
            return raw_data

        if isinstance(raw_data, bytes):
            raw_data = raw_data.decode("utf-8", errors="ignore")

        raw_data = raw_data.strip()

        if raw_data.startswith("<!DOCTYPE html>") or "<html" in raw_data.lower():
            raise RobloxAPIEdgeError("Roblox maintenance or Cloudflare challenge encountered.")

        if "Too Many Requests" in raw_data or "429" in raw_data[:50]:
            match = re.search(r'retry after (\d+)', raw_data, re.IGNORECASE)
            retry = int(match.group(1)) if match else 60
            raise RateLimitExceeded(retry_after=retry)

        try:
            parsed = json.loads(raw_data)
            return {default_key: parsed} if isinstance(parsed, list) else parsed
        except json.JSONDecodeError as e:
            match = re.search(r'(\{.*\}|\[.*\])', raw_data, re.DOTALL)
            if match:
                try:
                    res = json.loads(match.group(1))
                    return {default_key: res} if isinstance(res, list) else res
                except json.JSONDecodeError:
                    pass
            raise RobloxAPIEdgeError(f"Unrecoverable JSON payload: {e}")