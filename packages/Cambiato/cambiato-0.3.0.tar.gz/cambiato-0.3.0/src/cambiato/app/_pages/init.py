r"""The entry point of the initialization page."""

# Standard library
import logging
from pathlib import Path

# Third party
import streamlit as st
import streamlit_passwordless as stp

# Local
from cambiato import exceptions
from cambiato.app.config import (
    APP_HOME_PAGE_URL,
    APP_ISSUES_PAGE_URL,
    MAINTAINER_INFO,
)
from cambiato.app.controller.init import controller
from cambiato.config import load_config
from cambiato.database import create_session_factory

INIT_PATH = Path(__file__)

ABOUT = f"""Initialize the database of Cambiato and create an admin user.

{MAINTAINER_INFO}
"""

logger = logging.getLogger(__name__)


def init_page() -> None:
    r"""Run the initialization page of Cambiato."""

    st.set_page_config(
        page_title='Cambiato - Initialize',
        page_icon=':sparkles:',
        layout='wide',
        menu_items={
            'Get Help': APP_HOME_PAGE_URL,
            'Report a bug': APP_ISSUES_PAGE_URL,
            'About': ABOUT,
        },
    )

    try:
        cm = load_config()
    except exceptions.ConfigError as e:
        error_msg = f'Error loading configuration!\n{str(e)}'
        logger.error(error_msg)
        st.error(error_msg, icon=stp.ICON_ERROR)
        return

    cfg = cm.database
    session_factory = create_session_factory(
        url=cfg.url,
        autoflush=cfg.autoflush,
        expire_on_commit=cfg.expire_on_commit,
        create_database=True,
        connect_args=cfg.connect_args,
        **cfg.engine_config,
    )

    with session_factory() as session:
        controller(session=session, db_url=cfg.url)


if __name__ == '__main__' or __name__ == '__page__':
    init_page()
