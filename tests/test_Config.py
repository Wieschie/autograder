import pytest
import shutil
from jsonschema import ValidationError
from pathlib import Path

from autograder.Config import Config
from autograder.utils import libdir


@pytest.fixture
def datadir(tmpdir, request):
    """
    Adapted from: https://stackoverflow.com/a/29631801/1706825
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    """
    file = Path(request.module.__file__)
    test_dir = Path(file.stem)

    if test_dir.is_dir():
        shutil.copytree(test_dir, tmpdir)

    return tmpdir


def test_valid_file():
    config = Config(
        "sample_projects/complex_java/.config/config.toml",
        str((libdir() / "config_schema.json").absolute()),
    )


def test_invalid_file(datadir):
    for i in range(2):
        with pytest.raises(ValidationError):
            config = Config(
                datadir / f"config{i}.toml",
                str((libdir() / "config_schema.json").absolute()),
            )
