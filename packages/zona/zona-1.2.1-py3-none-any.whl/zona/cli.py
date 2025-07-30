from importlib.metadata import version as __version__
from pathlib import Path
from typing import Annotated

import typer

from zona import server
from zona.builder import ZonaBuilder
from zona.layout import initialize_site
from zona.log import get_logger, setup_logging

app = typer.Typer()
logger = get_logger()


@app.command()
def init(
    root: Annotated[
        Path | None,
        typer.Argument(
            help="Target directory to populate as a Zona project",
        ),
    ] = None,
):
    """
    Initialize a Zona website project.

    The required directory structure is created,
    and the default configuration file is included.

    Optionally specify the ROOT directory.
    """
    logger.info("Initializing site...")
    initialize_site(root)


@app.command()
def build(
    root: Annotated[
        Path | None,
        typer.Argument(
            help="Directory containing config.yml",
        ),
    ] = None,
    output: Annotated[
        Path | None,
        typer.Option(
            "--output", "-o", help="Location to write built website"
        ),
    ] = None,
    draft: Annotated[
        bool,
        typer.Option("--draft", "-d", help="Include drafts."),
    ] = False,
):
    """
    Build the website.

    Optionally specify the ROOT and OUTPUT directories.
    """
    if draft:
        print("Option override: including drafts.")
    builder = ZonaBuilder(
        cli_root=root, cli_output=output, draft=draft
    )
    builder.build()


@app.command()
def serve(
    root: Annotated[
        Path | None,
        typer.Argument(
            help="Directory containing config.yml",
        ),
    ] = None,
    host: Annotated[
        str,
        typer.Option(
            "--host", help="Hostname for live preview server."
        ),
    ] = "localhost",
    port: Annotated[
        int,
        typer.Option(
            "--port",
            "-p",
            help="Port number for live preview server.",
        ),
    ] = 8000,
    output: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Location to write built website. Temporary directory by default.",
        ),
    ] = None,
    final: Annotated[
        bool,
        typer.Option("--final", "-f", help="Don't include drafts."),
    ] = False,
    live_reload: Annotated[
        bool | None,
        typer.Option(
            "--live-reload/--no-live-reload",
            "-l/-L",
            help="Automatically reload web preview. Overrides config.",
            show_default=False,
        ),
    ] = None,
):
    """
    Build the website and start a live preview server.

    The website is rebuilt when the source is modified.

    Optionally specify the ROOT and OUTPUT directories.
    """
    if final:
        print("Preview without drafts.")
    else:
        print("Preview with drafts.")
    if live_reload is None:
        reload = None
    else:
        reload = live_reload
    server.serve(
        root=root,
        output=output,
        draft=not final,
        host=host,
        port=port,
        user_reload=reload,
    )


def version_callback(value: bool):
    if value:
        print(f"Zona version: {__version__('zona')}")
        raise typer.Exit()


@app.callback()
def main_entry(
    version: Annotated[  # pyright: ignore[reportUnusedParameter]
        bool | None,
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Print version info and exit.",
        ),
    ] = None,
    verbosity: Annotated[
        str,
        typer.Option(
            "--verbosity",
            "-v",
            help="Logging verbosity. One of INFO, DEBUG, WARN, ERROR.",
        ),
    ] = "info",
) -> None:
    """
    Opinionated static site generator.

    Supply --help after any subcommand for more details.
    """
    setup_logging(verbosity)


def main():
    app()
