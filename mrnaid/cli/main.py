import click
from mrnaid.cli.optimize import optimize_cli

@click.group()
def main():
    pass

# Register all commands
main.add_command(optimize_cli)
