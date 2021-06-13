from os import read
from typing import Optional, Union
from pathlib import Path
from tinydb import TinyDB
from utils import read_json


def init_db(db_path: Union[Path, str], json_path: Optional[Union[Path, str]] = None) -> TinyDB:
    db = TinyDB(db_path)
    if json_path:
        json_data = read_json(json_path)
        try:
            db.insert_multiple(json_data)
        except ValueError:
            raise ValueError("`json_path` must contain list of dictionaries")
    return db
