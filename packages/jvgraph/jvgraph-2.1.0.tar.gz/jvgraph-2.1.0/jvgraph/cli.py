"""Jivas Graph CLI tool."""

from jvgraph.commands.launch import launch
from jvgraph.group import jvgraph

# Register command groups
jvgraph.add_command(launch)


if __name__ == "__main__":
    jvgraph()  # pragma: no cover
