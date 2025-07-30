r"""The entry point of the Cambiato web app."""

# Standard library
from pathlib import Path

# Third party
import streamlit as st
import streamlit_passwordless as stp

# Local
from cambiato.app import auth
from cambiato.app._pages import Pages
from cambiato.app.components.sidebar import sidebar

APP_PATH = Path(__file__)


def main() -> None:
    r"""The page router of the Cambiato web app."""

    stp.init_session_state()
    authenticated = auth.authenticated()

    pages = [
        st.Page(page=Pages.HOME, title='Home'),
        st.Page(page=Pages.SIGN_IN, title='Sign in and register', default=True),
    ]
    page = st.navigation(pages, position='top' if authenticated else 'hidden')

    sidebar(authenticated=authenticated)

    page.run()


if __name__ == '__main__':
    main()
