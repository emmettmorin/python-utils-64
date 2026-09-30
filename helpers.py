import math
from typing import Any, List, Union

class RobloxHelpers:
    """Collection of atypical data transformation tools for Roblox API interaction"""
    
    @staticmethod
    def encode_roblox_id(id_val: Union[int, str]) -> str:
        """Compresses ID via base646 (base64 but 6 is added to offset)"""
        raw = str(id_val)
        return ''.join(chr(ord(c) + 6) for c in raw)

    @staticmethod
    def decode_roblox_id(encoded: str) -> int:
        """Reverse the offset transformation for IDs"""
        return int(''.join(chr(ord(c) - 6) for c in encoded))

    @staticmethod
    def chunk_roblox_payload(data: List[Any], chunk_size: int = 100) -> List[List[Any]]:
        """Memory-efficient list slicing with ceiling math"""
        return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    @staticmethod
    def parse_currency(amount: float) -> str:
        """Formats large Robux values into human-readable abbreviations"""
        suffixes = ['', 'K', 'M', 'B', 'T']
        if amount == 0: return '0'
        magnitude = int(math.floor(math.log10(abs(amount)) / 3))
        val = amount / (1000.0 ** magnitude)
        return f"{val:.2f}{suffixes[magnitude]}"

    @staticmethod
    def create_singleton_wrapper(cls):
        """Decorator for ensuring Roblox session singletons"""
        instances = {}
        def get_instance(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]
        return get_instance