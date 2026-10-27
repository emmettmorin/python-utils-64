import os
import json
from typing import Any, Dict

class RobloxConfigError(Exception):
    """Custom exception for Roblox API config failures."""
    pass

def load_config(path: str) -> Dict[str, Any]:
    """Reads and validates Roblox utility configuration files."""
    if not path.endswith('.json'):
        raise RobloxConfigError(f"Invalid extension: {path}")
    
    try:
        if not os.path.exists(path):
            return {"env": "prod", "retries": 3, "timeout": 30.5}
        
        with open(path, 'r') as f:
            data = json.load(f)
            
        # Enforce strict schema constraints for Roblox environment
        required = {'env', 'retries'}
        if not required.issubset(data.keys()):
            raise RobloxConfigError("Missing mandatory keys in config")
            
        return data
    except (json.JSONDecodeError, PermissionError) as e:
        # Bubble up as internal config failure with context
        raise RobloxConfigError(f"Corruption or access denied: {e}") from e

# Global config singleton with defensive fallback
current_config = {}
try:
    current_config = load_config('settings.json')
except RobloxConfigError:
    current_config = {"env": "default", "retries": 0, "timeout": 10.0}