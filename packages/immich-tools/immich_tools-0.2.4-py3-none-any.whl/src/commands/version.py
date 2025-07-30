import click
import src


@click.command()
def version():
    """shows version"""
    click.echo(src.__version__)
