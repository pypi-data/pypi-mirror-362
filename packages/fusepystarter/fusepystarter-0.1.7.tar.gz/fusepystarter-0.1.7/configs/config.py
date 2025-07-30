"""Load configuration using Dynaconf with environment and dotenv support."""

from pathlib import Path

from dynaconf import Dynaconf

_BASE_PATH = Path(__file__).parent.parent
_CONFIG_PATH = _BASE_PATH / "configs"

settings = Dynaconf(
    environments=True,
    envvar_prefix="DYNACONF",
    load_dotenv=True,
    settings_files=[_CONFIG_PATH / "settings.toml", _CONFIG_PATH / ".secrets.toml"],
    env_switcher="ENV_FOR_DYNACONF",
)
