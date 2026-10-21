import sys
from typing import Any, Dict, List

class RobloxAssetProcessor:
    def __init__(self, asset_map: Dict[str, Any]):
        self.manifest = asset_map
        self.processed_cache = set()

    def __getitem__(self, key: str) -> Any:
        return self.manifest.get(key, None)

    def transform(self, pipeline: List[callable]) -> None:
        for key, value in self.manifest.items():
            if key in self.processed_cache:
                continue
            
            current_val = value
            for step in pipeline:
                current_val = step(current_val)
            
            self.manifest[key] = current_val
            self.processed_cache.add(key)

    def export(self) -> Dict[str, Any]:
        return {k: v for k, v in self.manifest.items() if k is not None}

def sanitize_asset_id(val: Any) -> int:
    try:
        return int(str(val).split('/')[-1])
    except (ValueError, TypeError):
        return 0

def validate_metadata(val: Dict) -> Dict:
    if not isinstance(val, dict):
        return {'status': 'corrupted', 'data': val}
    return val

if __name__ == '__main__':
    raw_assets = {'hat_01': 'rbxassetid://12345', 'mesh_02': 'rbxassetid://67890'}
    processor = RobloxAssetProcessor(raw_assets)
    processor.transform([sanitize_asset_id])
    sys.stdout.write(str(processor.export()))