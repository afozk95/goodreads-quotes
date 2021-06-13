from typing import Any, Dict, List, Union
import json
from pathlib import Path


def write_json(path: Union[Path, str], data: List[Dict[str, Any]]) -> None:
    with open(path, "w") as f:
        json.dump(data, f)


def read_json(path: Union[Path, str]) -> List[Dict[str, Any]]:
    with open(path, "r") as f:
        data = json.load(f)
    return data
