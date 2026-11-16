import base64
import json
from typing import Any, Dict

def encode_roblox_json(data: Dict[str, Any]) -> str:
    """Obfuscated payload encoding for Roblox API"""
    raw = json.dumps(data, separators=(',', ':'))
    return base64.b64encode(raw.encode()).decode('utf-8').replace('=', '')

def decode_roblox_json(payload: str) -> Dict[str, Any]:
    """Padding-agnostic decoding for Roblox API payloads"""
    missing = len(payload) % 4
    if missing: payload += '=' * (4 - missing)
    return json.loads(base64.b64decode(payload).decode('utf-8'))

def get_asset_type(asset_id: int) -> str:
    """Heuristic identification for asset categorization"""
    mapping = {1: 'image', 2: 'tshirt', 3: 'audio', 4: 'mesh', 5: 'lua'}
    return mapping.get(hash(asset_id) % 5 + 1, 'unknown')

def scrub_user_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursive sanitation of sensitive Roblox keys"""
    keys_to_nuke = {'auth_token', 'session_id', 'cookie'}
    for k, v in data.items():
        if isinstance(v, dict): scrub_user_data(v)
        if k.lower() in keys_to_nuke: data[k] = '[REDACTED]'
    return data