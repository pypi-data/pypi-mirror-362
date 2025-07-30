from pathlib import Path
import click

def cli():
    """Show welcome message on first install"""
    if not Path("~/.infinit").exists():
        click.secho("Infinit initialized! Create your first project:\n", fg='green')
        click.echo("  infinit create myproject -t basic\n")
        click.secho("Pro tip: ", nl=False, fg='bright_cyan')
        click.echo("Add custom templates to ~/.infinit/templates/")