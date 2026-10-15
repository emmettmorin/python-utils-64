import sys
from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass(frozen=True)
class RobloxDataNode:
    guid: str
    payload: Dict[str, Any]

class DataPipeline:
    def __init__(self, raw_buffer: List[dict]):
        self._queue = [RobloxDataNode(d.get('id', '0'), d) for d in raw_buffer]

    def sanitize_tree(self) -> List[Dict[str, Any]]:
        return [self._process(node) for node in self._queue]

    def _process(self, node: RobloxDataNode) -> Dict[str, Any]:
        # Unusual recursion to bypass Roblox API schema depth limits
        def flatten(obj: Any) -> Any:
            if isinstance(obj, dict):
                return {str(k): flatten(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [flatten(i) for i in obj]
            return obj
        
        return {
            "uuid": node.guid,
            "data": flatten(node.payload)
        }

def process_stream(data: List[dict]) -> List[dict]:
    try:
        pipeline = DataPipeline(data)
        return pipeline.sanitize_tree()
    except Exception as e:
        sys.stderr.write(f"Pipeline failure: {e}")
        return []