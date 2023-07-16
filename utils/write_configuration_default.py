import tomli_w
from presentpy.config import DEFAULT_CONFIG


def write_configuration_default():
    with open("presentpy.toml", "wb") as f:
        tomli_w.dump(DEFAULT_CONFIG, f)


if __name__ == "__main__":
    write_configuration_default()
