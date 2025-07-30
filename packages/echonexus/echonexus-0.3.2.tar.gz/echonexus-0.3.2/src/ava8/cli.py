import click
from .composer import process_glyph_file, process_abc_file

@click.group()
def cli():
    """Ava8 Symphony CLI."""
    pass

@cli.command()
@click.argument('glyph_file')
@click.argument('output_midi')
def render(glyph_file, output_midi):
    """Render a glyph sequence file into a MIDI file."""
    process_glyph_file(glyph_file, output_midi)
    click.echo(f"MIDI written to {output_midi}")


@cli.command()
@click.argument('abc_file')
@click.argument('output_midi')
def render_abc(abc_file, output_midi):
    """Render an ABC notation file into a MIDI file."""
    process_abc_file(abc_file, output_midi)
    click.echo(f"MIDI written to {output_midi}")

if __name__ == '__main__':
    cli()
