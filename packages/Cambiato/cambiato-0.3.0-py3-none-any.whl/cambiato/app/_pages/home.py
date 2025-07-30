r"""The entry point of the home page."""

# Third party
import streamlit as st

# Local
from cambiato.app import auth
from cambiato.app._pages import Pages
from cambiato.app.config import (
    APP_HOME_PAGE_URL,
    APP_ISSUES_PAGE_URL,
    MAINTAINER_INFO,
)

ABOUT = f"""\
The simple yet powerful system for changing utility devices.

{MAINTAINER_INFO}
"""


@auth.authorized(redirect=Pages.SIGN_IN)
def home_page() -> None:
    r"""Run the home page of the Cambiato web app."""

    st.set_page_config(
        page_title='Cambiato - Home',
        page_icon=':cyclone:',
        layout='wide',
        menu_items={
            'About': ABOUT,
            'Get Help': APP_HOME_PAGE_URL,
            'Report a bug': APP_ISSUES_PAGE_URL,
        },
        initial_sidebar_state='auto',
    )

    st.title('Cambiato')
    st.subheader('The simple yet powerful system for changing utility devices')


if __name__ == '__main__' or __name__ == '__page__':
    home_page()
