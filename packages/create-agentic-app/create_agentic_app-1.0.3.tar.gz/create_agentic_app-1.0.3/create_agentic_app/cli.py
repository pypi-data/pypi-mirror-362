from importlib.resources import files

import click
from cookiecutter.main import cookiecutter


@click.command()
@click.argument('new_project')
def main(new_project):
    """Create a new agentic app project."""
    template_path = files("create_agentic_app").joinpath("template")
    click.echo(f"Creating new project: {new_project}")
    cookiecutter(
        template=str(template_path),
        no_input=True,
        extra_context={'project_name': new_project}
    )
