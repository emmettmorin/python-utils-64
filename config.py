import os
import json
from typing import Any, Dict, get_type_hints

class RobloxConfig:
    """
    A dynamic configuration loader for Roblox services.
    Coerces environment variables and file overrides based on class type hints.
    """
    universe_id: int = 0
    place_id: int = 0
    cookie: str = ""
    api_key: str = ""
    request_timeout: float = 10.0
    use_test_environment: bool = False

    def __init__(self, filepath: str = None, **overrides):
        self._values: Dict[str, Any] = {}
        self._load_defaults()
        if filepath and os.path.exists(filepath):
            self._load_from_file(filepath)
        self._load_from_env()
        for key, val in overrides.items():
            if val is not None:
                self._set_coerced(key, val)

    def _load_defaults(self):
        for key, value in self.__class__.__dict__.items():
            if not key.startswith("_") and not callable(value):
                self._set_coerced(key, value)

    def _load_from_file(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            for key, val in data.items():
                self._set_coerced(key, val)

    def _load_from_env(self):
        hints = get_type_hints(self.__class__)
        for key in hints:
            for prefix in ("ROBLOX_", "RBX_", ""):
                env_key = f"{prefix}{key.upper()}"
                if env_key in os.environ:
                    self._set_coerced(key, os.environ[env_key])
                    break

    def _set_coerced(self, key: str, value: Any):
        hints = get_type_hints(self.__class__)
        expected_type = hints.get(key, str)
        
        if key == "cookie" and isinstance(value, str):
            value = value.strip()
            warning_prefix = "_|WARNING:-DO NOT SHARE THIS.--Sharing this will allow someone to log in as you and steal your ROBUX and items.|_"
            if value and not value.startswith("_"):
                value = f"{warning_prefix}{value}"

        try:
            if expected_type is int:
                self._values[key] = int(value)
            elif expected_type is float:
                self._values[key] = float(value)
            elif expected_type is bool:
                self._values[key] = str(value).lower() in ("true", "1", "yes", "on")
            else:
                self._values[key] = expected_type(value)
        except (ValueError, TypeError):
            self._values[key] = value

    def __getattr__(self, name: str) -> Any:
        if name in self._values:
            return self._values[name]
        raise AttributeError(f"Configuration option {name!r} is not defined")

    def to_dict(self) -> Dict[str, Any]:
        return self._values.copy()