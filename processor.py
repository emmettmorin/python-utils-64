import re
from typing import Generator, Dict, Any, List

ROBLOX_ID_PATTERN = re.compile(r"^rbxassetid://(\d+)$|^(\d+)$")

class ValidationError(Exception):
    pass

def validate_roblox_task(task: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(task, dict):
        raise ValidationError("Task payload must be a dictionary")
    
    task_type = task.get("type")
    if task_type not in ("place_update", "asset_upload", "datastore_set"):
        raise ValidationError(f"Invalid task type: {task_type!r}")
        
    target_id = str(task.get("target_id", ""))
    match = ROBLOX_ID_PATTERN.match(target_id)
    if not match:
        raise ValidationError(f"Malformed Roblox Target ID: '{target_id}'")
        
    clean_id = int(match.group(1) or match.group(2))
    if clean_id <= 0:
        raise ValidationError(f"Roblox ID must be a positive integer: {clean_id}")

    data = task.get("data")
    if data is None:
        raise ValidationError("Task data payload cannot be None")
        
    return {
        "type": task_type,
        "target_id": clean_id,
        "data": data,
        "validated": True
    }

def process_roblox_queue(queue: List[Dict[str, Any]]) -> Generator[Dict[str, Any], None, None]:
    for raw_item in queue:
        try:
            validated_item = validate_roblox_task(raw_item)
            if validated_item["type"] == "asset_upload":
                validated_item["status"] = f"Uploaded to asset {validated_item['target_id']}"
            elif validated_item["type"] == "datastore_set":
                validated_item["status"] = f"Key set on universe {validated_item['target_id']}"
            else:
                validated_item["status"] = f"Processed place {validated_item['target_id']}"
            yield validated_item
        except ValidationError as err:
            yield {
                "raw_task": raw_item,
                "status": "rejected",
                "error": str(err)
            }
