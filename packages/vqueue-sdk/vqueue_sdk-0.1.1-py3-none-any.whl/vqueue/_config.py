from importlib import resources

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

with (resources.files("vqueue").joinpath("config.toml")).open("r") as config_file:
    _cfg = tomllib.loads(config_file.read())

API_BASE_PATH = _cfg["api"]["base_path"]
