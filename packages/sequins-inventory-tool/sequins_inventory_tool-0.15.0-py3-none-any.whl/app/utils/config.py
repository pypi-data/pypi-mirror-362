"""Load and save user configuration data."""

import tomlkit

from app.console import get_console
from app.constants import PACKAGE_NAME, PACKAGE_AUTHOR
from pathlib import Path
from platformdirs import user_config_path
from typing import Any, Dict, Optional

CONFIG_FILE_NAME = 'config.toml'


def get_config_dir() -> Path:
    """Returns the directory where user configuration files are stored."""
    return user_config_path(
        appname=PACKAGE_NAME, appauthor=PACKAGE_AUTHOR, ensure_exists=True
    )


def get_config_path() -> Path:
    return get_config_dir() / CONFIG_FILE_NAME


def load_config() -> Dict[str, Any]:
    """Loads the configuration from the local config file."""
    config_path = get_config_path()
    if not config_path.exists():
        return {}  # Return empty dict if file doesn't exist

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return tomlkit.parse(f.read())
    except (OSError, tomlkit.exceptions.TOMLKitError) as e:
        get_console().print(
            f'Warning: Could not load config file {config_path}. Error: {e}'
        )
        return {}


def save_config(config_data: Dict[str, Any]):
    """Saves the given configuration data to the local config file."""
    config_path = get_config_path()
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(tomlkit.dumps(config_data))
    except (OSError, tomlkit.exceptions.TOMLKitError) as e:
        get_console().print(
            f'Error: Could not save config file {config_path}. Error: {e}'
        )


def get_api_key() -> Optional[str]:
    """Retrieves the API key from the loaded configuration."""
    config = load_config()
    return config.get('api', {}).get('key')


def set_api_key_in_config(api_key: str):
    """Saves the API key to the configuration file."""
    config = load_config()
    if 'api' not in config:
        config['api'] = tomlkit.table()  # Create a TOML table for 'api' section
    config['api']['key'] = api_key
    save_config(config)
