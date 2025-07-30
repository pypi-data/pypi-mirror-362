import click
from infinit.core.scaffold import create_project

@click.command()
@click.argument("name")
@click.option("-t", "--template", default="basic", help="Template name")
@click.option("-v", "--verbose", is_flag=True, help="Show detailed output")
@click.option("-f", "--force", is_flag=True, help="Overwrite existing project")
def create(name, template, verbose, force):
    """Create a new project"""
    create_project(name, template, verbose=verbose, force=force)