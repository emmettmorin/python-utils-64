import json
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str, defaults: Dict[str, Any]):
        self.path = Path(path)
        self.defaults = defaults
        self._config = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.path.exists():
            self.path.write_text(json.dumps(self.defaults, indent=4))
            return self.defaults
        
        try:
            with open(self.path, 'r') as f:
                loaded = json.load(f)
                return {**self.defaults, **loaded}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def __getitem__(self, key: str) -> Any:
        return self._config.get(key)

    def __getattr__(self, name: str) -> Any:
        return self._config.get(name)

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self._config, f, indent=4)

    def update(self, **kwargs):
        self._config.update(kwargs)
        self.save()