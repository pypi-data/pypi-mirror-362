r"""The entry point of the Cambiato CLI."""

# Third party
import click

# Local
from cambiato.cli.commands.run import run
from cambiato.metadata import __releasedate__

COMMANDS = (run,)


@click.group(
    name='cambiato',
    context_settings={'help_option_names': ['-h', '--help'], 'max_content_width': 1000},
)
@click.version_option(
    message=(
        f'%(prog)s, version: %(version)s, release date: {__releasedate__}, maintainer: Anton Lydell'
    )
)
def main() -> None:
    r"""Manage the Cambiato application."""


for cmd in COMMANDS:
    main.add_command(cmd)

if __name__ == '__main__':
    main()
