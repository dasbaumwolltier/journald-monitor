from typing import Any, Dict, List, TypeVar, Union

T = TypeVar('T', str, int, float, Dict[str, Any], List[Any], None)
def get_from_dict(d: dict, key: str, default_value: T) -> T:
    current = d

    for part in key.split('.'):
        if part in current:
            current = current[part]
        else:
            return default_value

    return current

def call_function(object):
    pass
