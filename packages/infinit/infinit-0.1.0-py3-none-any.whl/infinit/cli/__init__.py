import click
from infinit.cli.create import create
from infinit.cli.template import template_cmd

@click.group()
def cli():
    pass

cli.add_command(create, name="create")
cli.add_command(template_cmd, name="template")

if __name__ == "__main__":
    cli()