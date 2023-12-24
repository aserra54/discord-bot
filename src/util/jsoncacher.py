import json
import os
from datetime import datetime, timedelta
from typing import NamedTuple


class JsonFileInfo(NamedTuple):
    '''Structure containing the JSON data of a file, as well as when it was last
    accessed.'''
    data: dict
    last_accessed: datetime


# Mapping of normalized file paths to their corresponding data
_DATA: dict[str, JsonFileInfo] = {}

# The amount of time that must pass for data to be considered stale
_EXPIRE_TIME = timedelta(hours=24)


def get(path: str) -> dict:
    '''Gets the JSON data at the specified path. If the data has already been
    cached, then the cached data will be returned; otherwise, the file will be
    loaded from disk and cached.'''

    path_key = os.path.abspath(path)
    file_info = _DATA.get(path_key, None)
    if file_info is not None:
        new_file_info = JsonFileInfo(data=file_info.data,
                                     last_accessed=datetime.now())
        _DATA[path_key] = new_file_info
        return new_file_info.data

    with open(path_key, mode='r', encoding='utf-8') as f:
        raw_data = f.read()
    json_data = json.loads(raw_data)
    file_info = JsonFileInfo(data=json_data, last_accessed=datetime.now())
    _DATA[path_key] = file_info
    return json_data


def update() -> None:
    '''Updates the cache to remove any data that has not been accessed for a
    significant period of time.'''

    current_time = datetime.now()
    to_purge = []

    for path, file_info in _DATA.items():
        delta = current_time - file_info.last_accessed
        if delta > _EXPIRE_TIME:
            to_purge.append(path)

    for path in to_purge:
        del _DATA[path]
