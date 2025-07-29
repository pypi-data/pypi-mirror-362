import click
from .utils import test_connection

@click.group()
def cli():
    """cwtoken command-line interface."""
    pass

cli.add_command(test_connection, name="test-connection")

if __name__ == "__main__":
    cli()
