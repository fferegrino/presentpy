from copy import deepcopy

from presentpy.config.read_only_dot_dict import ReadOnlyDotDict

DEFAULT_CONFIG = {
    "font-size": 16,
    "highlight": {
        "font-size": 18,
        "bold": True,
    },
}


def get_configuration():
    config = deepcopy(DEFAULT_CONFIG)
    # config.update(read_configuration())
    return ReadOnlyDotDict(config)
