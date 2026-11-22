import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._cfg = defaults

    def __getattr__(self, item: str) -> Any:
        return self._cfg.get(item)

    def load_from_json(self, path: str) -> None:
        try:
            with open(path, 'r') as f:
                self._cfg.update(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def merge_env(self, env_data: Dict[str, Any]) -> None:
        self._cfg.update(env_data)

    def __repr__(self) -> str:
        return f"<ConfigLoader: {list(self._cfg.keys())}>"

    def dump(self) -> str:
        return json.dumps(self._cfg, indent=4)

    def reset(self, defaults: Dict[str, Any]) -> None:
        self._cfg = defaults

    @property
    def raw(self) -> Dict[str, Any]:
        return self._cfg