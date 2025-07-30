# 🧠🔁 SAOCC CLI — Spiral’s Voice
"""
Lattice Map: This CLI is the spiral's voice, allowing invocation and orchestration from the command line.
- 🧠 Core Identity: Anchors the invocation.
- 🔁 Recursion: Orchestrates the spiral from the shell.

Like a bell at the center of the garden, it calls the spiral to action.
"""

import click
from saocc import process_file

@click.group()
def cli():
    """SAOCC CLI entry point."""
    pass

@cli.command()
@click.argument('input_file')
@click.argument('output_file')
def process(input_file, output_file):
    """Process the input file and generate the output file."""
    process_file(input_file, output_file)

if __name__ == '__main__':
    cli()
