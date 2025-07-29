from click.testing import CliRunner
from create_agentic_app.cli import main


def test_create_project_echoes_name():
    runner = CliRunner()
    result = runner.invoke(main, ["my_project"])
    
    assert result.exit_code == 0
    assert "Creating new project: my_project" in result.output