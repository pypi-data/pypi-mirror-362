r"""The configuration of Cambiato."""

from cambiato.config.config import ConfigManager, load_config
from cambiato.config.core import (
    BITWARDEN_PASSWORDLESS_API_URL,
    CONFIG_DIR,
    CONFIG_FILE_ENV_VAR,
    CONFIG_FILE_PATH,
    CONFIG_FILENAME,
    PROG_NAME,
    BaseConfigModel,
    BitwardenPasswordlessConfig,
    DatabaseConfig,
    Language,
)
from cambiato.config.log import (
    LOGGING_DEFAULT_DATETIME_FORMAT,
    LOGGING_DEFAULT_DIR,
    LOGGING_DEFAULT_FILE_PATH,
    LOGGING_DEFAULT_FILENAME,
    LOGGING_DEFAULT_FORMAT,
    LOGGING_DEFAULT_FORMAT_DEBUG,
    EmailLogHandler,
    FileLogHandler,
    LoggingConfig,
    LogHanderType,
    LogHandler,
    LogLevel,
    Stream,
    StreamLogHandler,
)

# The Public API
__all__ = [
    # config
    'ConfigManager',
    'load_config',
    # core
    'BITWARDEN_PASSWORDLESS_API_URL',
    'CONFIG_DIR',
    'CONFIG_FILE_ENV_VAR',
    'CONFIG_FILE_PATH',
    'CONFIG_FILENAME',
    'PROG_NAME',
    'BaseConfigModel',
    'BitwardenPasswordlessConfig',
    'DatabaseConfig',
    'Language',
    # log
    'LOGGING_DEFAULT_DATETIME_FORMAT',
    'LOGGING_DEFAULT_DIR',
    'LOGGING_DEFAULT_FILE_PATH',
    'LOGGING_DEFAULT_FILENAME',
    'LOGGING_DEFAULT_FORMAT',
    'LOGGING_DEFAULT_FORMAT_DEBUG',
    'EmailLogHandler',
    'FileLogHandler',
    'LoggingConfig',
    'LogHanderType',
    'LogHandler',
    'LogLevel',
    'Stream',
    'StreamLogHandler',
]
