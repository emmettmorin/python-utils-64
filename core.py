import sys
import threading
from typing import Dict, Any, Tuple, List

class FastRobloxInstance:
    """
    Thread-safe optimized instance builder leveraging custom slot pools
    and string interning to optimize memory and property lookup speed
    when parsing heavy Roblox model files (RBXL/RBXM).
    """
    _class_cache: Dict[Tuple[str, Tuple[str, ...]], type] = {}
    _lock = threading.Lock()

    @classmethod
    def build(cls, class_name: str, data: Dict[str, Any]) -> Any:
        # Intern class name and keys to save memory and optimize lookup
        interned_name = sys.intern(class_name)
        sorted_keys = tuple(sys.intern(k) for k in sorted(data.keys()))
        cache_key = (interned_name, sorted_keys)

        with cls._lock:
            optimized_class = cls._class_cache.get(cache_key)
            if not optimized_class:
                optimized_class = type(
                    f"Fast_{interned_name}",
                    (object,),
                    {"__slots__": sorted_keys, "ClassName": interned_name}
                )
                cls._class_cache[cache_key] = optimized_class

        instance = optimized_class()
        for key, value in data.items():
            setattr(instance, sys.intern(key), value)
        return instance

    @classmethod
    def bulk_build(cls, records: List[Tuple[str, Dict[str, Any]]]) -> List[Any]:
        # Micro-optimized bulk processing loop using localized lookups
        build_func = cls.build
        return [build_func(class_name, data) for class_name, data in records]
