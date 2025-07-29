import os
import re
from pathlib import Path


def load_template(template_name: str) -> str:
    """Load a template from the templates directory, adding .tpl if not present."""
    template_dir = Path(__file__).parent / "templates"
    if not template_name.endswith(".tpl"):
        template_name += ".tpl"
    template_path = template_dir / template_name

    if not template_path.exists():
        raise FileNotFoundError(
            f"Template '{template_name}' not found in {template_dir}"
        )

    with open(template_path, "r") as f:
        return f.read()


def substitute_template(template_content: str, **variables) -> str:
    """Substitute variables in template content using %%VARNAME%% syntax."""
    result = template_content

    for var_name, var_value in variables.items():
        pattern = f"%%{var_name}%%"
        result = result.replace(pattern, str(var_value))

    return result


def load_and_substitute(template_name: str, **variables) -> str:
    """Load a template and substitute variables in one step."""
    template_content = load_template(template_name)
    return substitute_template(template_content, **variables)
