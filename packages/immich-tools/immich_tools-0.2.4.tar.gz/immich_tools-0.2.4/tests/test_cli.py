import pytest
from click.testing import CliRunner
from src.cli import main


@pytest.fixture
def runner():
    return CliRunner()


def test_main_help(runner):
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "This is immich-tools version" in result.output


def test_main_refresh_album_metadata_commands_registered(runner):
    result = runner.invoke(main, ["refresh-album-metadata", "--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_main_merge_xmp_command_registered(runner):
    result = runner.invoke(main, ["merge-xmp", "--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_main_run_job_command_registered(runner):
    result = runner.invoke(main, ["run-job", "--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_main_version_command_registered(runner):
    result = runner.invoke(main, ["version", "--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_main_check_album_tags_command_registered(runner):
    result = runner.invoke(main, ["check-album-tags", "--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
