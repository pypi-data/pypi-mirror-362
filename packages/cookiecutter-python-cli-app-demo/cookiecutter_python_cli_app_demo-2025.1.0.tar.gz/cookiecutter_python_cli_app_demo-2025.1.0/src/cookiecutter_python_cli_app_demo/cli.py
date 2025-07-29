"""Main CLI for cookiecutter-python-cli-app-demo."""

from importlib import metadata

import click


@click.command(
    context_settings={"help_option_names": ["-h", "--help"], "show_default": True}
)
@click.argument("input_", metavar="INPUT")
@click.option(
    "-r",
    "--reverse",
    is_flag=True,
    help="Reverse the input.",
)
@click.version_option(
    metadata.version("cookiecutter_python_cli_app_demo"), "-v", "--version"
)
def cli(input_: str, *, reverse: bool = False) -> None:
    """Repeat the input.

    Demo of https://github.com/sgraaf/cookiecutter-python-cli-app.
    """
    click.echo(input_ if not reverse else input_[::-1])
