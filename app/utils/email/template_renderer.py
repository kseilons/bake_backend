# template_renderer.py
import os
from jinja2 import Template

current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'template'))

def render_template(template_name: str, context: dict) -> str:
    with open(os.path.join(template_path, template_name), 'r') as file:
        template = Template(file.read())
    return template.render(context)

