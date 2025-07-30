r"""The ConfigManager and the config loading functions."""

# Standard library
import os
import sys
import tomllib
from pathlib import Path

# Third party
from pydantic import AliasChoices, ConfigDict, Field

# Local
from cambiato import exceptions
from cambiato.config.core import (
    CONFIG_FILE_ENV_VAR,
    CONFIG_FILE_PATH,
    BaseConfigModel,
    BitwardenPasswordlessConfig,
    DatabaseConfig,
    Language,
)
from cambiato.config.log import LoggingConfig


class ConfigManager(BaseConfigModel):
    r"""Handles the configuration of Cambiato.

    Parameters
    ----------
    config_file_path : Path or None, default None
        The path to the config file from which the configuration was loaded.
        The special path '-' specifies that the config was loaded from stdin.
        If None the default configuration was loaded.

    language : cambiato.Language, default cambiato.Language.EN
        The default language to use when starting the application. The default is English.

    database : cambiato.DatabaseConfig
        The database configuration.

    bwp : cambiato.BitwardenPasswordlessConfig
        The configuration for Bitwarden Passwordless.dev.

    logging : cambiato.LoggingConfig
        The logging configuration.
    """

    model_config = ConfigDict(frozen=True)

    config_file_path: Path | None = None
    language: Language = Language.EN
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    bwp: BitwardenPasswordlessConfig = Field(
        validation_alias=AliasChoices('bwp', 'bitwarden_passwordless', 'bitwarden_passwordless_dev')
    )
    logging: LoggingConfig = Field(default_factory=LoggingConfig)


def _load_config_from_stdin() -> str:
    r"""Load the configuration from stdin."""

    content = ''

    if not sys.stdin.isatty():  # Content piped to stdin.
        for line in sys.stdin:
            content = f'{content}\n{line}'

    return content


def _load_config_from_file(path: Path) -> str:
    r"""Load the configuration from a config file."""

    content = ''

    if path.is_dir():
        error_msg = f'The config file "{path}" must be a file not a directory!'
        raise exceptions.ConfigFileNotFoundError(message=error_msg, data=path)

    if path == CONFIG_FILE_PATH:
        if path.exists():
            content = path.read_text()
    elif not path.exists():
        raise exceptions.ConfigFileNotFoundError(
            message=f'The config file "{path}" does not exist!', data=path
        )
    else:
        content = path.read_text()

    return content


def load_config(path: Path | None = None) -> ConfigManager:
    r"""Load the configuration of Cambiato.

    The configuration can be loaded from four different sources listed
    below in the order in which they will override each other:

    1. A specified config file to `path` parameter.

    2. From stdin by specifying the `path` `pathlib.Path('-')`.

    3. A config file specified in environment variable "CAMBIATO_CONFIG_FILE".

    4. From the default config file location "~/.config/Cambiato/Cambiato.toml".

    5. If none of the above the default configuration will be loaded.

    Parameters
    ----------
    path : pathlib.Path or None, default None
        The path to the config file. Specify `Path('-')` for stdin. If None the configuration
        will be loaded from the config file environment variable "CAMBIATO_CONFIG_FILE" if it
        exists otherwise from the default config file at "~/.config/Cambiato/Cambiato.toml".
        If none of these sources exist stdin will be searched for configuration and if no
        configuration is found :exc:`cambiato.ConfigError` will be raised.

    Returns
    -------
    ConfigManager
        An instance of the program's configuration.

    Raises
    ------
    cambiato.ConfigError
        If the configuration is invalid or if no configuration was found.

    cambiato.ConfigFileNotFoundError
        If the configuration file could not be found.

    cambiato.ParseConfigError
        If there are syntax errors in the config file.
    """

    file_path: Path | None = None
    file_path_str = ''
    config_content = ''

    if path is None:
        if (_file_path := os.getenv(CONFIG_FILE_ENV_VAR)) is None:
            file_path = CONFIG_FILE_PATH
        else:
            file_path = Path(_file_path)
    elif path.name == '-':  # stdin
        file_path = None
    else:
        file_path = path

    if file_path is not None:
        config_content = _load_config_from_file(path=file_path)
        file_path_str = str(file_path)

    if not config_content:
        config_content = _load_config_from_stdin()
        file_path_str = '-'

    if not config_content:
        raise exceptions.ConfigError('No configuration found! Check your sources!')

    config_content = f"config_file_path = '{file_path_str}'\n{config_content}"

    try:
        config_from_toml = tomllib.loads(config_content)
    except (tomllib.TOMLDecodeError, TypeError) as e:
        error_msg = f'Syntax error in config : {e.args[0]}'
        raise exceptions.ParseConfigError(error_msg) from None

    return ConfigManager.model_validate(config_from_toml)
