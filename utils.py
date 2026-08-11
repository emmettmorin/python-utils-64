import json
from typing import Any, Dict, List, Union

def flatten_json(y: Union[Dict[str, Any], List[Any]]) -> Dict[str, Any]:
    out = {}

    def flatten(x: Union[Dict, List], name: str = ''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '_')
        elif isinstance(x, list):
            for i, a in enumerate(x):
                flatten(a, name + str(i) + '_')
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def read_json_file(filepath: str) -> Dict[str, Any]:
    with open(filepath, 'r') as file:
        return json.load(file)

def write_json_file(filepath: str, data: Dict[str, Any]) -> None:
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)