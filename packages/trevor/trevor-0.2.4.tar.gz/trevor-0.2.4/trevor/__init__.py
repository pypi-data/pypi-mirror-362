import click
from trevor.cli import cosmosdb

@click.group(help='A CLI tool for managing Azure resources.')
def cli():
    pass

cli.add_command(cosmosdb.cli, name='cosmosdb')

if __name__ == '__main__':
    cli()
