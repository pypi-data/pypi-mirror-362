import click
from saocc.cli import cli as saocc_cli
from upkeys.cli import cli as upkeys_cli
from cadro.cli import cli as cadro_cli
from ava8.cli import cli as ava8_cli
from ai.semiotic_cli import cli as semiotic_cli
from ai.speclang_cli import cli as speclang_cli

@click.group()
def main():
    """Unified EchoNexus CLI."""
    pass

main.add_command(saocc_cli, name='saocc')
main.add_command(upkeys_cli, name='upkeys')
main.add_command(cadro_cli, name='cadro')
main.add_command(ava8_cli, name='ava8')
main.add_command(semiotic_cli, name='semiotic')
main.add_command(speclang_cli, name='speclang')

if __name__ == '__main__':
    main()
