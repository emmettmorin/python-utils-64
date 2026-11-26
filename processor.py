import base64
import zlib
import json

def encode_rbx_payload(data: dict) -> str:
    raw = json.dumps(data).encode('utf-8')
    return base64.b64encode(zlib.compress(raw)).decode('utf-8')

def decode_rbx_payload(payload: str) -> dict:
    raw = base64.b64decode(payload.encode('utf-8'))
    return json.loads(zlib.decompress(raw).decode('utf-8'))

def format_roblox_instance_path(path: str) -> list:
    return [p.strip() for p in path.split('/') if p]

def sanitize_identifier(name: str) -> str:
    return ''.join(c if c.isalnum() or c == '_' else '_' for c in name)

def generate_service_proxy(service_name: str) -> str:
    return f"game:GetService('{service_name}')"