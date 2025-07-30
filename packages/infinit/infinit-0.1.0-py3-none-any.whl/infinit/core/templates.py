from pathlib import Path
import yaml
from infinit.core.exceptions import TemplateValidationError, TemplateNotFoundError

REQUIRED_FIELDS = {"name", "folders"}

def _init_user_template_dir():
    template_dir = Path.home() / ".infinit" / "templates"
    try:
        template_dir.mkdir(parents=True, mode=0o700, exist_ok=True)  # drwx------ 
        (template_dir / "README").write_text("# Infinit user templates\n")
    except OSError as e:
        raise OSError(f"Couldn't create template dir: {e}")

def find_template(template_name: str) -> Path:
    """Search for template in all possible locations."""
    search_locations = [
        Path.home() / ".infinit" / "templates" / f"{template_name}.yaml",
        Path(__file__).parent.parent / "templates" / f"{template_name}.yaml",
    ]    
    
    # Check for direct path
    if "/" in template_name or template_name.startswith("~"):
        path = Path(template_name).expanduser()
        if path.exists():
            return path
        raise TemplateNotFoundError(f"Template '{template_name}' not found")

    # Check default locations
    for location in search_locations:
        if location.exists():
            return location
    

    raise TemplateNotFoundError(
        f"Template '{template_name}' not found in:\n"
        f"- {search_locations[0]}\n"
        f"- {search_locations[1]}"
    )

def list_all_templates(verbose: bool = False) -> list:
    """Returns template names or (name, path) pairs.
    
    Args:
        verbose: If True, returns tuples of (name, path). Else returns names only.
    """
    tepmplate_locations = [
        Path.home() / ".infinit" / "templates", # User templates
        Path(__file__).parent.parent / "templates" # Default templates
    ]

    found = {}
    
    for location in tepmplate_locations:
        if location.exists():
            for yaml_file in location.glob("*.yaml"):
                if yaml_file.stem not in found:
                    found[yaml_file.stem] = yaml_file

    if verbose:
        return [(name, path) for name, path in found.items()]
    return sorted(found.keys())

def validate_template(config: dict):
    """Validate template structure"""
    if not isinstance(config, dict):
        raise TemplateValidationError("Template must be a dictionary")
   
    errors = []
    
    # Check required fields
    missing = REQUIRED_FIELDS - set(config.keys())
    if missing:
        errors.append(f"Missing required keys: {missing}")
    
    # Validate fields (if present)
    if "folders" in config and not isinstance(config["folders"], list):
        errors.append("'folders' must be a list")
        
    if "files" in config:
        if not isinstance(config["files"], dict):
            errors.append("'files' must be a dict")
        else:
            for path, content in config["files"].items():
                if not isinstance(content, str):
                    errors.append(f"File '{path}' content must be string")
    
    if errors:
        raise TemplateValidationError("\n".join(errors))
    
def load_template(template_name: str) -> dict:
    """Load template from first found location."""
    _init_user_template_dir()  # Ensure user template dir exists
    template_path = find_template(template_name)
    try:
        config = yaml.safe_load(template_path.read_text())
        if not config:
            raise TemplateValidationError(f"Template file is empty: {template_path}")
        validate_template(config)
        return config
    except yaml.YAMLError as e:
        raise TemplateValidationError(f"Invalid YAML in {template_path}: {e}")
    """Save template to user's template directory."""
    user_templates_dir = Path.home() / ".infinit" / "templates"
    user_templates_dir.mkdir(parents=True, exist_ok=True)
    (user_templates_dir / f"{name}.yaml").write_text(content)