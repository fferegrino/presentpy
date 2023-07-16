import collections.abc
from copy import deepcopy
from pathlib import Path

import tomli

from presentpy.config.read_only_dot_dict import ReadOnlyDotDict

DEFAULT_CONFIG = {
    "font-size": 16,
    "highlight": {
        "font-size": 18,
        "bold": True,
    },
}

CONFIGURATION_FILE = "presentpy.toml"


def recursive_update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = recursive_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def find_configuration_file_path():
    if Path(CONFIGURATION_FILE).exists():
        return Path(CONFIGURATION_FILE)
    if Path(Path.home(), CONFIGURATION_FILE).exists():
        return Path(Path.home(), CONFIGURATION_FILE)
    if Path(Path.home(), f".{CONFIGURATION_FILE}").exists():
        return Path(Path.home(), CONFIGURATION_FILE)
    return None


def get_configuration():
    config = deepcopy(DEFAULT_CONFIG)

    if file := find_configuration_file_path():
        with open(file, "rb") as f:
            config = recursive_update(config, tomli.load(f))

    return ReadOnlyDotDict(config)
