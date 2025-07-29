import json
import yaml
from typing import Callable, Dict, Any
from pathlib import Path

def load_menu_structure(path: str, callbacks: Dict[str, Callable]) -> Dict[str, Any]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Menu file '{path}' does not exist.")

    if path.suffix == ".json":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    elif path.suffix in {".yaml", ".yml"}:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    else:
        raise ValueError("Unsupported file format. Use .json or .yaml")

    return resolve_callbacks(data, callbacks)

def resolve_callbacks(struct: Dict, callbacks: Dict[str, Callable]) -> Dict:
    def _resolve(obj):
        if isinstance(obj, dict):
            resolved = {}
            for k, v in obj.items():
                if k == "__action__" and isinstance(v, str) and v in callbacks:
                    resolved[k] = callbacks[v]
                else:
                    resolved[k] = _resolve(v)
            return resolved
        elif isinstance(obj, list):
            return [_resolve(x) for x in obj]
        return obj

    return _resolve(struct)
