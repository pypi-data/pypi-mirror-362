import click
from pathlib import Path
from .semiotic_cli import load_engine

# Specs live at the project root
SPEC_DIR = Path(__file__).resolve().parents[2] / 'specs'

@click.group()
def cli():
    """Helpers for writing SpecLang files."""
    pass

@cli.command()
@click.argument('name')
@click.option('--component', help='Component to pull roles from Semiotic Engine')
def new(name, component):
    """Create a new spec template."""
    SPEC_DIR.mkdir(exist_ok=True)
    path = SPEC_DIR / f"{name}.spec.md"
    lines = [f"# {name} Spec", "", "This spec is written in SpecLang."]
    if component:
        engine = load_engine()
        roles = engine.get_roles(component)
        if roles:
            lines.extend(["", f"## Roles for {component}"])
            lines.extend([f"- {r}" for r in roles])
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    click.echo(f"Created {path}")

if __name__ == '__main__':
    cli()
