import sys
from typing import Dict, Type, Any

class RobloxException(Exception):
    """Base exception for the python-utils-64 suite."""
    pass

class CacheOverflowError(RobloxException):
    pass

_EXCEPTION_CACHE: Dict[str, Type[RobloxException]] = {}

def _memoize_exception(cls: Type[RobloxException]) -> Type[RobloxException]:
    _EXCEPTION_CACHE[cls.__name__] = cls
    return cls

@_memoize_exception
class DataModelError(RobloxException):
    pass

@_memoize_exception
class ServiceUnavailable(RobloxException):
    pass

def raise_optimized(exc_name: str, message: str) -> None:
    """
    Raises a cached exception instance to minimize memory allocation overhead
    during heavy Roblox API polling cycles.
    """
    target_cls = _EXCEPTION_CACHE.get(exc_name, RobloxException)
    raise target_cls(message) from None

def get_exception_registry() -> Dict[str, Type[RobloxException]]:
    return _EXCEPTION_CACHE