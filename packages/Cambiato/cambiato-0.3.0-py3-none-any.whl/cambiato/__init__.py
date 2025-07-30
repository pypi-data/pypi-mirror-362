r"""The Cambiato package.

Cambiato is the simple yet powerful system for changing utility
devices such as district heating and electricity meters.
"""

# Local
from cambiato import database as db
from cambiato.app import APP_PATH
from cambiato.config import (
    BITWARDEN_PASSWORDLESS_API_URL,
    CONFIG_DIR,
    CONFIG_FILE_ENV_VAR,
    CONFIG_FILE_PATH,
    CONFIG_FILENAME,
    LOGGING_DEFAULT_DATETIME_FORMAT,
    LOGGING_DEFAULT_DIR,
    LOGGING_DEFAULT_FILE_PATH,
    LOGGING_DEFAULT_FILENAME,
    LOGGING_DEFAULT_FORMAT,
    LOGGING_DEFAULT_FORMAT_DEBUG,
    PROG_NAME,
    BitwardenPasswordlessConfig,
    ConfigManager,
    DatabaseConfig,
    EmailLogHandler,
    FileLogHandler,
    Language,
    LoggingConfig,
    LogHanderType,
    LogHandler,
    LogLevel,
    Stream,
    StreamLogHandler,
    load_config,
)
from cambiato.exceptions import (
    CambiatoError,
    ConfigError,
    ConfigFileNotFoundError,
    ParseConfigError,
)
from cambiato.log import setup_logging
from cambiato.metadata import (
    __releasedate__,
    __version__,
    __versiontuple__,
)

# The Public API
__all__ = [
    # app
    'APP_PATH',
    # metadata
    '__releasedate__',
    '__version__',
    '__versiontuple__',
    # config
    'BITWARDEN_PASSWORDLESS_API_URL',
    'CONFIG_DIR',
    'CONFIG_FILE_ENV_VAR',
    'CONFIG_FILE_PATH',
    'CONFIG_FILENAME',
    'LOGGING_DEFAULT_DATETIME_FORMAT',
    'LOGGING_DEFAULT_DIR',
    'LOGGING_DEFAULT_FILE_PATH',
    'LOGGING_DEFAULT_FILENAME',
    'LOGGING_DEFAULT_FORMAT',
    'LOGGING_DEFAULT_FORMAT_DEBUG',
    'PROG_NAME',
    'BitwardenPasswordlessConfig',
    'ConfigManager',
    'DatabaseConfig',
    'EmailLogHandler',
    'FileLogHandler',
    'Language',
    'LoggingConfig',
    'LogHanderType',
    'LogHandler',
    'LogLevel',
    'Stream',
    'StreamLogHandler',
    'load_config',
    # database
    'db',
    # exceptions
    'CambiatoError',
    'ConfigError',
    'ConfigFileNotFoundError',
    'ParseConfigError',
    # log
    'setup_logging',
]
