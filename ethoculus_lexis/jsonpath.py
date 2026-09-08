from typing import Any


def extract_dot_path(data: Any, path: str) -> Any:
    """
    Extract a value from nested dictionaries using a dot path.

    Example:
        extract_dot_path(data, "result.answer.text")
    """
    if not path:
        return data

    current = data

    for part in path.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None

        if current is None:
            return None

    return current
