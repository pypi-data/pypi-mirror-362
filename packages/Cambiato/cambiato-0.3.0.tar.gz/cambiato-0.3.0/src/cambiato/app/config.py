r"""The configuration of the Cambiato web app."""

# Third party
import streamlit_passwordless as stp

# Local
from cambiato.metadata import __releasedate__, __version__

MAINTAINER_INFO = f"""\
- Maintainer   : [*Anton Lydell*](https://github.com/antonlydell)
- Version      : {__version__}
- Release date : {__releasedate__}"""

APP_HOME_PAGE_URL = 'https://github.com/antonlydell/Cambiato'
APP_ISSUES_PAGE_URL = 'https://github.com/antonlydell/Cambiato/issues'

ICON_INFO = stp.ICON_INFO
ICON_SUCCESS = stp.ICON_SUCCESS
ICON_WARNING = stp.ICON_WARNING
ICON_ERROR = stp.ICON_ERROR
