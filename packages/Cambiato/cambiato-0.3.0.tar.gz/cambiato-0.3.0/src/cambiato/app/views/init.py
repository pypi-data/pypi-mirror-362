r"""The views of the init page."""

# Third party
import streamlit as st
import streamlit_passwordless as stp

# Local
from cambiato import database as db


def title() -> None:
    r"""Render the title view of the init page."""

    st.title('Initialize Cambiato')
    st.divider()


@st.cache_resource()
def initialize(_session: db.Session, db_url: db.URL) -> None:
    r"""Render the initialize view of the init page.

    Initialize the database with the default data and
    warn the user if the database is already initialized.

    Parameters
    ----------
    _session : cambiato.db.Session
        An active session to the database to initialize.

    db_url : cambiato.db.URL
        The database url of the database being initialized.
    """

    error, error_msg = db.init(session=_session)

    if error:
        message = f'Database "{db_url}" already initialized! {error_msg}'
        st.warning(message, icon=stp.ICON_WARNING)
    else:
        st.success(f'Successfully initialized database : "{db_url}"!', icon=stp.ICON_SUCCESS)

    st.divider()


def create_admin_user(session: db.Session) -> None:
    r"""Render the create admin user view of the init page.

    Parameters
    ----------
    session : cambiato.db.Session
        An active session to the database to initialize.
    """

    stp.create_user_form(
        db_session=session,
        with_ad_username=True,
        with_custom_roles=False,
        role_preselected=3,
        title='Create admin user',
    )
