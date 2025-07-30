r"""Initialize a database with the default data."""

# Standard library
import logging

# Third party
import streamlit_passwordless as stp

# Local
from cambiato.database.core import Session, commit
from cambiato.database.models import add_default_models_to_session

logger = logging.getLogger(__name__)


def init(session: Session) -> tuple[bool, str]:
    r"""Initialize a database with the default data models.

    Parameters
    ----------
    session : sqlalchemy.orm.Session
        An active database session.

    Returns
    -------
    error : bool
        True if a :exc:`streamlit_passwordless.DatabaseError` occurred and the database
        could not be initialized correctly and False for no error.

    error_msg : str
        An error message that is safe to display to the user. An empty
        string is returned if `error` is False.
    """

    error = False
    error_msg = ''

    stp.db.create_default_roles(session=session, commit=False)
    add_default_models_to_session(session=session)

    try:
        commit(session=session, error_msg='Error initializing database!')
    except stp.DatabaseError as e:
        error = True
        error_msg = e.displayable_message
        logger.warning(e.detailed_message)
        session.rollback()

    return error, error_msg
