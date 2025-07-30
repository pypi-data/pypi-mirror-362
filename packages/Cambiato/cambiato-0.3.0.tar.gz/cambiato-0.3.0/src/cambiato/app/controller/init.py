r"""The controller of the init page."""

# Local
from cambiato.app.views.init import create_admin_user, initialize, title
from cambiato.database.core import URL, Session


def controller(session: Session, db_url: URL) -> None:
    r"""Render the init page.

    Parameters
    ----------
    session : cambiato.db.Session
        An active session to the Cambiato database.

    db_url : cambiato.db.URL
        The database url of the database to initialize.
    """

    title()
    initialize(_session=session, db_url=db_url)
    create_admin_user(session=session)
