r"""The page controller of the sign in page."""

# Third party
import streamlit as st
import streamlit_passwordless as stp

# Local
from cambiato.app._pages import Pages
from cambiato.database import Session


def controller(
    session: Session, client: stp.BitwardenPasswordlessClient, authenticated: bool = False
) -> None:
    r"""Render the sign in and register page.

    Parameters
    ----------
    session : cambiato.db.Session
        An active session to the Cambiato database.

    client : streamlit_passwordless.BitwardenPasswordlessClient
        The client for interacting with the backend API of Bitwarden Passwordless.dev.

    authenticated : bool
        True if the user is authenticated and False otherwise.
    """

    st.title('Cambiato')

    with st.container(border=True):
        if authenticated:
            stp.bitwarden_register_form_existing_user(
                client=client, db_session=session, border=False
            )
        else:
            stp.bitwarden_register_form(
                client=client,
                db_session=session,
                pre_authorized=True,
                with_displayname=False,
                with_email=False,
                border=False,
                redirect=Pages.HOME,
            )
        st.write('Already have an account?')
        stp.bitwarden_sign_in_button(
            client=client, db_session=session, with_autofill=True, redirect=Pages.HOME
        )
