r"""The entry point of the sub-command run.

Run the Cambiato web apps.
"""

# Standard library
import subprocess
from pathlib import Path
from typing import Iterable

# Third party
import click

# Local
from cambiato.app._pages.init import INIT_PATH
from cambiato.app.main import APP_PATH

streamlit_args_argument = click.argument('streamlit_args', nargs=-1, type=click.UNPROCESSED)


def run_streamlit_app(path: Path | str, streamlit_args: Iterable[str]) -> None:
    r"""Run a Streamlit application.

    Parameters
    ----------
    path : Path or str
        The path to the module with the Streamlit application to run.

    streamlit_args : Iterable[str]
        Additional arguments to pass along to Streamlit.
    """

    run_cmd = ['python', '-m', 'streamlit', 'run', str(path) if isinstance(path, Path) else path]
    run_cmd.extend(streamlit_args)

    click.echo('Launching Streamlit ...')
    subprocess.run(run_cmd)


@click.group()
def run() -> None:
    """Run the Streamlit apps of Cambiato.

    \b
    Configuring Streamlit
    ---------------------
    Streamlit can be configured with config files, environment variables or command line options.
    Below is a list of the configuration options in order in which they will override each
    other:

    1 : Command line options.

    2 : Environment variables with names of the config options prefixed by STREAMLIT, e.g. STREAMLIT_SERVER_PORT

    3 : A local config file located in the current working directory at "./.streamlit/config.toml".

    4 : A global config file located in the user's home directory at: "~/.streamlit/config.toml"

    See also the Streamlit documentation on configuration for more details:
    https://docs.streamlit.io/library/advanced-features/configuration#view-all-configuration-options

    \b
    Examples
    --------
    Run the Cambiato web app and pass on command line options to Streamlit:
        $ cambiato run web --theme.base dark --server.headless true
    """


@run.command(context_settings={'ignore_unknown_options': True})
@streamlit_args_argument
def web(streamlit_args: tuple[str, ...]) -> None:
    """Run the Cambiato web app."""

    run_streamlit_app(path=APP_PATH, streamlit_args=streamlit_args)


@run.command(context_settings={'ignore_unknown_options': True})
@streamlit_args_argument
def init(streamlit_args: tuple[str, ...]) -> None:
    """Initialize the Cambiato database and create an admin user."""

    run_streamlit_app(path=INIT_PATH, streamlit_args=streamlit_args)
