import click
import yaml

from infinit.core.templates import (
    list_all_templates,
    load_template,
)
from infinit.core.exceptions import TemplateNotFoundError, TemplateValidationError

@click.command(name="template", help="Manage project templates")
@click.argument("path_or_name", required=False)
@click.option("--list", "-l", is_flag=True, help="List available templates")
@click.option("--verbose", "-v", is_flag=True, help="Show template details")
def template_cmd(path_or_name, list, verbose):
    try:
        if list:
            # List all templates
            templates = list_all_templates(verbose=verbose)
            if verbose:
                for name, path in templates:
                    click.echo(f"{name}: {path}")
            else:
                click.echo("\n".join(templates))
            return

        if not path_or_name:
            raise click.UsageError("Specify template path/name or use --list")

        config = load_template(path_or_name)
        if verbose:
            click.echo(yaml.dump(config))
        click.secho("✓ Valid template", fg="green")

    except TemplateNotFoundError as e:
        click.secho(f"🚨 Template not found: {e}", fg="red", err=True)
    except TemplateValidationError as e:
        click.secho(f"❌ Invalid template: {e}", fg="red", err=True)
    except Exception as e:
        click.secho(f"💥 Unexpected error: {e}", fg="red", err=True)
        raise click.Abort()