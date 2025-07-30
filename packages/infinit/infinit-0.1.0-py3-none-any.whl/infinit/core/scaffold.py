from pathlib import Path
import shutil

import click
from infinit.core.templates import load_template

from pathlib import Path
from infinit.core.templates import load_template, TemplateNotFoundError

def create_project(name: str, template: str, verbose: bool = False, force: bool = False) -> None:
    """Generate folder structure."""
    try:
        project_path = Path(name).absolute()
        
        if project_path.exists():
            if force:
                click.secho(f"\n[!] Force overwriting ", nl=False, fg='yellow')
                click.secho(f"'{name}'", fg='bright_white', bold=True)
                shutil.rmtree(project_path)
            else:
                raise FileExistsError(f"Directory '{name}' already exists")

        config = load_template(template)
        
        click.secho(f"\n[+] Creating ", nl=False, fg='green')
        click.secho(f"'{name}'", fg='bright_white', bold=True, nl=False)
        click.secho(" using template: ", nl=False)
        click.secho(template, fg='bright_cyan', bold=True)

        try:
            _create_folders(project_path, config.get("folders", []), verbose=verbose)
            _create_files(project_path, config.get("files", {}), verbose=verbose)
        except Exception as e:
            _cleanup_on_failure(project_path)
            raise  # Re-raise for outer handler

    except TemplateNotFoundError:
        click.secho("\n[!] Template not found. Try:", fg='red')
        click.secho("  infinit template --list", fg='bright_white')
        raise click.Abort()
    except FileExistsError as e:
        click.secho(f"\n[!] {e}", fg='yellow')
        click.secho("  Use --force to overwrite", dim=True)
        raise click.Abort()
    except Exception as e:
        click.secho(f"\n[!] Failed: {e}", fg='red')
        raise click.Abort()

def _cleanup_on_failure(path: Path) -> None:
    """Remove partially created project on failure."""
    try:
        if path.exists():
            shutil.rmtree(path)
    except Exception:
        pass  # Don't mask original error


def _create_folders(base_path: Path, folders: list[str], verbose: bool) -> None:
    """Create all required folders."""
    for folder in folders:
        folder_path = base_path / folder
        folder_path.mkdir(parents=True)
        
        click.secho("[+] Created: ", fg='green', nl=False)
        if verbose:
            click.secho(str(folder_path), fg='bright_cyan', dim=True)
        else:
            click.secho(folder, fg='bright_white')

def _create_files(base_path: Path, files: dict[str, str], verbose: bool) -> None:
    """Create all files with content."""
    for file_path, content in files.items():
        full_path = base_path / file_path
        full_path.parent.mkdir(parents=True)
        full_path.write_text(content.strip())

        if file_path.endswith('.sh'):
            full_path.chmod(0o755)

        click.secho("[+] Created: ", fg='green', nl=False)
        if verbose:
            click.secho(str(full_path), fg='bright_cyan', dim=True)
        else:
            click.secho(file_path, fg='bright_white')