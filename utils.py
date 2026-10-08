import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Union

def parse_roblox_xml(xml_content: Union[str, bytes]) -> List[Dict[str, Any]]:
    """
    Parses Roblox XML asset format (.rbxmx / .rbxlx) dynamically into nested Python dicts,
    handling complex properties like Vector3, Color3, and CFrame coordinates natively.
    """
    if isinstance(xml_content, str):
        xml_content = xml_content.encode("utf-8")
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError:
        return []

    def _extract_props(props_node: ET.Element) -> Dict[str, Any]:
        data = {}
        for child in props_node:
            name = child.get("name")
            if not name:
                continue
            tag = child.tag.lower()
            if tag in ("string", "protectedstring"):
                data[name] = child.text or ""
            elif tag == "bool":
                data[name] = (child.text or "").strip().lower() == "true"
            elif tag in ("int", "int64", "float", "double"):
                val = (child.text or "0").strip()
                data[name] = float(val) if "float" in tag or "double" in tag else int(val)
            elif tag in ("vector3", "color3", "vector2"):
                data[name] = {c.tag.upper(): float(c.text or 0) for c in child}
            elif tag == "coordinateframe":
                # Extracts all sub-coordinate components under CFrame representation
                data[name] = [float(val.text or 0) for val in child]
            else:
                data[name] = child.text
        return data

    def _parse_item(item_node: ET.Element) -> Dict[str, Any]:
        props = {}
        props_node = item_node.find("Properties")
        if props_node is not None:
            props = _extract_props(props_node)
        
        children = [_parse_item(child) for child in item_node if child.tag == "Item"]
        return {
            "class_name": item_node.get("class", "Instance"),
            "referent": item_node.get("referent", ""),
            "properties": props,
            "children": children
        }

    items = []
    # Handle root level and direct nested Items
    target_root = root if root.tag == "Item" else root.findall(".//Item")
    
    if root.tag == "Item":
        items.append(_parse_item(root))
    else:
        for top_level in root:
            if top_level.tag == "Item":
                items.append(_parse_item(top_level))
                
    return items