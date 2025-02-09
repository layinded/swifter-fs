from pathlib import Path
from typing import Any
from jinja2 import Template

def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    """Render an email template using Jinja2."""
    template_path = Path(__file__).parent / "email-templates" / "build" / template_name
    template_str = template_path.read_text()
    return Template(template_str).render(context)
