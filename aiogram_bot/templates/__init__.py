import re

from jinja2 import Environment, FileSystemLoader

from config import TEMPLATES_DIR

env = Environment(
    loader=FileSystemLoader(searchpath=TEMPLATES_DIR),
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=True
)


def render_template(template_name: str, data: dict | None = None) -> str:
    if data is None:
        data = {}

    template = env.get_template(template_name)
    rendered = template.render(**data)
    rendered = rendered.replace("\n", " ")
    rendered = rendered.replace("<br>", "\n")
    rendered = re.sub(" +", " ", rendered).replace(" .", ".").replace(" ,", ",")
    rendered = "\n".join(line.strip() for line in rendered.split("\n"))

    return rendered
