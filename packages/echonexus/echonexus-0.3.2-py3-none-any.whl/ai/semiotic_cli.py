import json
import os
from pathlib import Path
import click
from .semiotic_table_engine import SemioticTableEngine

# Reach project root so the registry lives in examples/semiotic/
REGISTRY_FILE = Path(__file__).resolve().parents[2] / 'examples' / 'semiotic' / 'registry.json'

def load_engine():
    engine = SemioticTableEngine()
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, 'r') as f:
            data = json.load(f)
        for component, roles in data.items():
            engine.register(component, roles)
    return engine

def save_engine(engine):
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_FILE, 'w') as f:
        json.dump(engine.registry, f, indent=2)

@click.group()
def cli():
    """Manage the Semiotic Table Engine."""
    pass

@cli.command()
@click.argument('component')
@click.argument('roles', nargs=-1)
def register(component, roles):
    """Register COMPONENT with symbolic ROLES."""
    engine = load_engine()
    engine.register(component, roles)
    save_engine(engine)
    click.echo(f"Registered {component} -> {roles}")

@cli.command('list-components')
def list_components():
    """List all registered components."""
    engine = load_engine()
    for comp in engine.all_components():
        click.echo(comp)

@cli.command('get-roles')
@click.argument('component')
def get_roles(component):
    """Show roles for COMPONENT."""
    engine = load_engine()
    roles = engine.get_roles(component)
    click.echo(', '.join(roles) if roles else '(none)')

if __name__ == '__main__':
    cli()
