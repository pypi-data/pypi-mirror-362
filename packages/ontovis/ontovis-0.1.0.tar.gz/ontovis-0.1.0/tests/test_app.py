import pytest
from typer.testing import CliRunner

from ontovis.main import app

runner = CliRunner()


@pytest.mark.slow
def test_entrypoint_remote_file():
    result = runner.invoke(
        app,
        [
            "render",
            # an XML-document with only the root element, base64-encoded
            "https://httpbin.org/base64/PD94bWwgdmVyc2lvbj0iMS4wIj8+CjxwYXRoYnVpbGRlcmludGVyZmFjZS8+",
        ],
    )
    assert result.exit_code == 0


def test_entrypoint_local_file():
    result = runner.invoke(app, ["render", "./tests/fixtures/fixture.xml"])
    assert result.exit_code == 0


def test_raw():
    result = runner.invoke(app, ["render", "./tests/fixtures/fixture.xml", "--raw"])
    assert result.exit_code == 0


def test_entrypoint_local_file_disabled_paths():
    result = runner.invoke(
        app, ["render", "./tests/fixtures/fixture_disabled-path.xml"]
    )
    assert result.exit_code == 0
