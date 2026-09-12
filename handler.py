import xml.etree.ElementTree as ET
from typing import Dict, Any, Union, List

class RobloxAssetNode:
    """Dynamically translates Roblox XML elements into pythonic schemas."""
    def __init__(self, element: ET.Element):
        self._element = element
        self.classname = element.attrib.get("class", "Unknown")
        self.referent = element.attrib.get("referent", "")
        self.properties = self._parse_properties(element.find("Properties"))

    def _parse_properties(self, properties_node: Union[ET.Element, None]) -> Dict[str, Any]:
        if properties_node is None:
            return {}
        
        parsed = {}
        type_map = {
            "string": str,
            "bool": lambda val: val.strip().lower() == "true",
            "float": float,
            "int": int,
            "double": float,
        }
        
        for prop in properties_node:
            name = prop.attrib.get("name")
            if not name:
                continue
            
            tag_cast = type_map.get(prop.tag.lower())
            if tag_cast:
                parsed[name] = tag_cast(prop.text) if prop.text else None
            elif prop.tag.lower() == "vector3":
                coords = {c.tag.lower(): float(c.text or 0) for c in prop}
                parsed[name] = (coords.get("x", 0.0), coords.get("y", 0.0), coords.get("z", 0.0))
            else:
                parsed[name] = prop.text or "".join(prop.itertext()).strip()
                
        return parsed

    def __repr__(self) -> str:
        return f"<RobloxAssetNode class='{self.classname}' properties={list(self.properties.keys())}>"


def parse_rbxmx_properties(xml_string: str) -> List[RobloxAssetNode]:
    """Parses a raw rbxmx string and yields representation node objects."""
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError:
        return []
        
    nodes = []
    for item in root.findall(".//Item"):
        nodes.append(RobloxAssetNode(item))
    return nodes
