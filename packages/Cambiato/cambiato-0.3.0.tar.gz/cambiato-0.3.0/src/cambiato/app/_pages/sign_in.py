r"""The entry point of the sign in page."""

# Standard library
from pathlib import Path

# Third party
import streamlit as st

# Local
from cambiato.app import auth
from cambiato.app.config import (
    APP_HOME_PAGE_URL,
    APP_ISSUES_PAGE_URL,
    MAINTAINER_INFO,
)
from cambiato.app.controller.sign_in import controller
from cambiato.app.setup import bwp_client, session_factory

SIGN_IN_PATH = Path(__file__)

ABOUT = f"""Sign in to Cambiato or register an account.

{MAINTAINER_INFO}
"""


def sign_in_page() -> None:
    r"""Run the sign in page of Cambiato."""

    authenticated = auth.authenticated()
    st.set_page_config(
        page_title='Cambiato - Sign in',
        page_icon=':sparkles:',
        layout='centered',
        menu_items={
            'Get Help': APP_HOME_PAGE_URL,
            'Report a bug': APP_ISSUES_PAGE_URL,
            'About': ABOUT,
        },
        initial_sidebar_state='auto' if authenticated else 'collapsed',
    )

    with session_factory() as session:
        controller(session=session, client=bwp_client, authenticated=authenticated)


if __name__ == '__main__' or __name__ == '__page__':
    sign_in_page()
