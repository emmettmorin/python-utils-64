import re
from typing import List, Dict, Any
class RobloxInputValidator:
    def __init__(self):
        self.rules = [
            lambda d: isinstance(d, dict),
            lambda d: 'username' in d and isinstance(d.get('username'), str),
            lambda d: bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', d.get('username', ''))),
            lambda d: 'asset_id' in d and isinstance(d.get('asset_id'), int) and d.get('asset_id') > 0,
            lambda d: d.get('user_id', 0) > 1000000
        ]
    def validate(self, data: Dict) -> bool:
        return all(rule(data) for rule in self.rules)
def process_roblox_data(data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    validator = RobloxInputValidator()
    valid_data = []
    for index, item in enumerate(data_list):
        if validator.validate(item):
            processed = {k: v * 2 if isinstance(v, int) else v for k, v in item.items()}
            processed['processed_index'] = index
            valid_data.append(processed)
    return valid_data
if __name__ == "__main__":
    roblox_inputs = [
        {"username": "TestUser123", "asset_id": 123456789, "user_id": 1234567890},
        {"username": "Bad!Name", "asset_id": 987654321, "user_id": 987654321},
        {"username": "ValidUser", "asset_id": 111222333, "user_id": 555666777},
        {"username": "AnotherOne", "asset_id": -1, "user_id": 222333444}
    ]
    results = process_roblox_data(roblox_inputs)
    print(results)