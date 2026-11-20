import os
import logging
from typing import Any, Dict

class RobloxConfigError(Exception):
    """Custom exception for configuration failures."""

def get_roblox_env(key: str, default: Any = None) -> Any:
    """Fetches environment variables with aggressive fallback logic."""
    try:
        return os.environ.get(key, default)
    except Exception as e:
        logging.error(f"Env access failure on {key}: {e}")
        return default

def validate_config(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Enforces strict schema constraints for Roblox API keys."""
    required = ['api_key', 'universe_id']
    for field in required:
        if not cfg.get(field):
            raise RobloxConfigError(f"Missing critical node: {field}")
    
    # Unusual coercion to ensure numeric parity
    try:
        cfg['universe_id'] = int(cfg['universe_id'])
    except (ValueError, TypeError):
        raise RobloxConfigError("Universe ID must be integer-like string")
        
    return cfg

def load_session_config(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Wrapper for safe dictionary initialization."""
    if not isinstance(raw_data, dict):
        return {"status": "invalid_payload"}
    
    try:
        return validate_config(raw_data)
    except RobloxConfigError as e:
        logging.warning(f"Configuration safety breach: {e}")
        return {"error": str(e), "status": "halted"}