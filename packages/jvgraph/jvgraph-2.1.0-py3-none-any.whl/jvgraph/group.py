"""Jivas Graph CLI tool."""

import click

from jvgraph import __version__


@click.group()
@click.version_option(__version__, prog_name="jvgraph")
def jvgraph() -> None:
    """Jivas Graph CLI tool."""
    pass  # pragma: no cover
