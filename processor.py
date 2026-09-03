import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Union

class InstanceProcessor:
    """
    A utility to generate Roblox XML Model (.rbxmx) structures from highly
    flexible, structural Python dictionary templates.
    """
    TYPE_MAPPING = {
        float: "float",
        int: "int64",
        str: "string",
        bool: "bool"
    }

    @classmethod
    def _build_properties(cls, parent_element: ET.Element, properties: Dict[str, Any]) -> None:
        properties_node = ET.SubElement(parent_element, "Properties")
        for key, val in properties.items():
            val_type = type(val)
            
            # Map compound geometric representations creatively
            if isinstance(val, (tuple, list)) and len(val) == 3:
                node = ET.SubElement(properties_node, "Vector3", name=key)
                for idx, axis in enumerate(["X", "Y", "Z"]):
                    ET.SubElement(node, axis).text = str(float(val[idx]))
            elif isinstance(val, dict) and "R" in val and "G" in val and "B" in val:
                node = ET.SubElement(properties_node, "Color3", name=key)
                for color_channel in ["R", "G", "B"]:
                    ET.SubElement(node, color_channel).text = str(float(val[color_channel]))
            elif val_type in cls.TYPE_MAPPING:
                node_type = cls.TYPE_MAPPING[val_type]
                node = ET.SubElement(properties_node, node_type, name=key)
                node.text = str(val).lower() if isinstance(val, bool) else str(val)

    @classmethod
    def to_rbxmx(cls, instance_tree: Dict[str, Any]) -> str:
        """
        Transforms a python-dict tree of Roblox instances into an importable .rbxmx string.
        
        Example tree format:
        {
            "class": "Part",
            "properties": {"Name": "SpawnPart", "Anchored": True, "Position": (0, 50, -12)},
            "children": []
        }
        """
        root = ET.Element("roblox", xmlns="http://www.roblox.com/roblox", version="4")
        
        def process_node(parent: ET.Element, node_dict: Dict[str, Any]) -> None:
            cls_name = node_dict.get("class", "Folder")
            ref = f"RBX{abs(hash(frozenset(node_dict.items())) if not isinstance(node_dict, dict) else id(node_dict))}"
            node_elem = ET.SubElement(parent, "Item", attrib={"class": cls_name, "referent": ref})
            
            cls._build_properties(node_elem, node_dict.get("properties", {}))
            
            for child in node_dict.get("children", []):
                process_node(node_elem, child)

        process_node(root, instance_tree)
        return ET.tostring(root, encoding="utf-8", xml_declaration=False).decode("utf-8")