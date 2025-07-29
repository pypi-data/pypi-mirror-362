from typing import Dict, Callable, List, Union
from difflib import get_close_matches

MenuAction = Union[Callable, dict]

def search_menu(structure: Dict[str, MenuAction], query: str, fuzzy: bool = True, path: List[str] = []) -> List[str]:
    results = []

    for key, value in structure.items():
        full_path = path + [key]

        if fuzzy:
            if get_close_matches(query.lower(), [key.lower()], n=1, cutoff=0.6):
                results.append(" → ".join(full_path))
        else:
            if query.lower() in key.lower():
                results.append(" → ".join(full_path))

        if isinstance(value, dict):
            results += search_menu(value, query, fuzzy=fuzzy, path=full_path)

    return results
