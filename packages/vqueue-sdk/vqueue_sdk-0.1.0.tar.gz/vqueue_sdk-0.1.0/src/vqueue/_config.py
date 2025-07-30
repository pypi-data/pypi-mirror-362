from importlib import resources

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

_cfg = tomllib.loads(resources.read_text("vqueue", "config.toml"))

API_BASE_PATH = _cfg["api"]["base_path"]
