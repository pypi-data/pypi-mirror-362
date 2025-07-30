r"""User authentication and authorization."""

# Third party
import streamlit as st
import streamlit_passwordless as stp
from streamlit_passwordless import authorized as authorized

# Local
from cambiato.app.session_state import AUTHENTICATED


def authenticated(user: stp.User | None = None) -> bool:
    r"""Check if the current user is authenticated.

    Parameters
    ----------
    user : streamlit_passwordless.User or None, default None
        The user for which to check the authentication status.
        The default option is to fetch the current user from the
        session state.
    """

    if st.session_state.get(AUTHENTICATED, False) is True:
        return True

    user = stp.get_current_user() if user is None else user

    return user is not None and user.is_authenticated
