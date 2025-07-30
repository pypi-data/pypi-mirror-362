r"""The core config models."""

# Standard library
import logging
from enum import StrEnum
from pathlib import Path
from typing import Any

# Third party
import streamlit_passwordless as stp
from pydantic import AnyHttpUrl, Field, field_validator
from sqlalchemy import URL

# Local
from cambiato import exceptions
from cambiato.models.core import BaseModel

logger = logging.getLogger(__name__)


PROG_NAME = 'Cambiato'

CONFIG_DIR = Path.home() / '.config' / PROG_NAME

CONFIG_FILENAME = f'{PROG_NAME}.toml'

CONFIG_FILE_PATH = CONFIG_DIR / CONFIG_FILENAME

CONFIG_FILE_ENV_VAR = 'CAMBIATO_CONFIG_FILE'

BITWARDEN_PASSWORDLESS_API_URL = stp.BITWARDEN_PASSWORDLESS_API_URL


class Language(StrEnum):
    r"""The available languages of Cambiato."""

    EN = 'English'
    SV = 'Swedish'


class BaseConfigModel(BaseModel):
    r"""The base model that all configuration models inherit from."""

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        try:
            super().__init__(**kwargs)
        except exceptions.CambiatoError as e:
            raise exceptions.ConfigError(str(e)) from None


class DatabaseConfig(BaseConfigModel):
    r"""The database configuration for Cambiato.

    Parameters
    ----------
    url : str or sqlalchemy.URL, default 'sqlite:///Cambiato.db'
        The SQLAlchemy database url of the Cambiato database.

    autoflush : bool, default False
        Automatically flush pending changes within the session
        to the database before executing new SQL statements.

    expire_on_commit : bool, default False
        If True make the connection between the models and the database expire
        after a transaction within a session has been committed and if False make
        the database models accessible after the commit.

    create_database : bool, default True
        If True the database table schema will be created if it does not exist.

    connect_args : dict[Any, Any], default dict()
        Additional arguments sent to the database driver upon
        connection that further customizes the connection.

    engine_config : dict[str, Any], default dict()
        Additional keyword arguments passed to the :func:`sqlalchemy.create_engine` function.
    """

    url: str | URL = Field(default='sqlite:///Cambiato.db', validate_default=True)
    autoflush: bool = False
    expire_on_commit: bool = False
    create_database: bool = True
    connect_args: dict[Any, Any] = Field(default_factory=dict)
    engine_config: dict[str, Any] = Field(default_factory=dict)

    @field_validator('url')
    @classmethod
    def validate_url(cls, url: str | URL) -> stp.db.URL:
        r"""Validate the database url."""

        try:
            return stp.db.create_db_url(url)
        except stp.DatabaseInvalidUrlError as e:
            raise ValueError(f'{type(e).__name__} : {e!s}') from None


class BitwardenPasswordlessConfig(BaseConfigModel):
    r"""The configuration for Bitwarden Passwordless.dev.

    Bitwarden Passwordless.dev handles the passkey registration and authentication.

    Parameters
    ----------
    public_key : str, default ''
         The public key of the Bitwarden Passwordless.dev backend API.

    private_key : str, default ''
         The private key of the Bitwarden Passwordless.dev backend API.

    url : pydantic.AnyHttpUrl or str, default default 'https://v4.passwordless.dev'
        The base url of the backend API of Bitwarden Passwordless.dev. Specify this url
        if you are self-hosting Bitwarden Passwordless.dev.
    """

    public_key: str
    private_key: str
    url: AnyHttpUrl = stp.BITWARDEN_PASSWORDLESS_API_URL
