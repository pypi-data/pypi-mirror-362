r"""Sidebar components."""

# Third party
import streamlit as st
import streamlit_passwordless as stp

# Local
from cambiato.app.session_state import AUTHENTICATED


def sidebar(authenticated: bool) -> None:
    r"""Render the sidebar.

    Parameters
    ----------
    authenticated : bool
        True if the user is authenticated and False otherwise.
    """

    if not authenticated:
        return

    with st.sidebar:
        if stp.sign_out_button():
            st.session_state[AUTHENTICATED] = False
