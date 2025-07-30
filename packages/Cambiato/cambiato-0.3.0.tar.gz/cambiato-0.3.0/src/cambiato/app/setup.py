r"""Setup the resources needed by the Cambiato web app."""

# Standard library
import logging

# Third party
import streamlit as st
import streamlit_passwordless as stp

# Local
from cambiato import exceptions
from cambiato.app.config import ICON_ERROR
from cambiato.config import load_config
from cambiato.database import create_session_factory
from cambiato.log import setup_logging

logger = logging.getLogger(__name__)


try:
    cm = load_config()
except exceptions.ConfigError as e:
    logger.error(e.detailed_message)
    st.error('Error loading configuration! Check the logs for more details.', icon=ICON_ERROR)
    st.stop()

setup_logging(config=cm.logging)

try:
    session_factory = create_session_factory(
        url=cm.database.url,
        autoflush=cm.database.autoflush,
        expire_on_commit=cm.database.expire_on_commit,
        create_database=True,
        connect_args=cm.database.connect_args,
        **cm.database.engine_config,
    )
except exceptions.SQLAlchemyError as e:
    logger.error(f'Error creating session factory:\n{e!s}')
    st.error('Error connecting to database! Check the logs for more details.', icon=ICON_ERROR)
    st.stop()

bwp_client = stp.BitwardenPasswordlessClient(
    public_key=cm.bwp.public_key, private_key=cm.bwp.private_key
)
