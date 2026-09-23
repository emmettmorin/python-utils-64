import json
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    """Dynamic attribute access for Roblox bot configurations."""
    def __init__(self, file_path: str, defaults: Dict[str, Any]):
        self._path = Path(file_path)
        self._data = defaults
        self._load()

    def _load(self) -> None:
        if self._path.exists():
            with open(self._path, 'r') as f:
                try:
                    self._data.update(json.load(f))
                except json.JSONDecodeError:
                    pass

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value
            self._save()

    def _save(self) -> None:
        with open(self._path, 'w') as f:
            json.dump(self._data, f, indent=4)

    def __repr__(self) -> str:
        return f"<ConfigLoader: {list(self._data.keys())}>"

def get_config(name: str = "config.json", **defaults) -> ConfigLoader:
    return ConfigLoader(name, defaults)