from typer.testing import CliRunner

from iron_cardio.__init__ import __version__
from iron_cardio.__main__ import cli

runner = CliRunner()


def test_version():
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert f"{__version__}\n" in result.stdout


def test_session():
    result = runner.invoke(cli, ["session"])
    assert result.exit_code == 0
    assert "Iron Cardio Session" in result.stdout
    assert "===================" in result.stdout
    assert "Bells: " in result.stdout
    assert "Variation: " in result.stdout
    assert "Time: " in result.stdout
    assert "Load: " in result.stdout
