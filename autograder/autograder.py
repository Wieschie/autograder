"""
Command line utility to launch automatic grading of programming assignments
"""

import sys

import click
import shlex
from datetime import datetime as dt
from jsonschema import ValidationError
from pathlib import Path
from shutil import copy

import utils
from Config import Config
from TestResult import TestResult
from TestRunner import TestRunner


@click.group()
@click.version_option("1.2.1")
def cli():
    """ Launch automatic grading of programming assignments """
    pass


@cli.command()
def init():
    """ Generate a skeleton config directory """
    try:
        (Path(".") / ".config").mkdir(exist_ok=False)
    except FileExistsError:
        click.confirm(
            ".config directory already exists. "
            "Would you like to overwrite config.toml?",
            abort=True,
        )
    copy(str(utils.libdir() / "config.toml"), Path(".").absolute() / ".config")


@cli.command()
def testall():
    """ Build and test all projects """
    __test(utils.walk_subdirs("."))


@cli.command(short_help="Build and test one or more specified projects")
@click.argument("directories", nargs=-1, required=True)
def test(directories):
    """
    Build and test one or more specified projects. Followed by space-delimited list of
    relative subdirectories.
    """
    __test(directories)


def __test(directories):
    """
    Takes a list of directories, initialises results storage, loads config, and
    calls runtest on each directory.
    """
    results_dir = Path(".") / ".results" / dt.now().strftime("%Y-%m-%dT%H-%M-%S")
    results_dir.mkdir(exist_ok=True, parents=True)
    config = load_config()
    for d in directories:
        runtest(config, Path(d), results_dir)


def load_config() -> Config:
    config = None
    try:
        config = Config(
            ".config/config.toml",
            str((utils.libdir() / "config_schema.json").absolute()),
        )
    except FileNotFoundError:
        print("No config file found.  Are you in the root directory of a project?")
        sys.exit(1)
    except ValidationError as e:
        print(f"Invalid config file:\n{e.message}")
        sys.exit(1)
    return config


def runtest(config: Config, workdir: Path, results_dir: Path):
    print(f"========== Grading {workdir.name} ==========")

    (workdir / config["output_dir"]).mkdir(exist_ok=True, parents=True)
    secret_files = []
    with (results_dir / workdir.name).open("w", encoding="utf-8") as logfile:
        if "build" in config:
            logfile.write(utils.box_text("Build Step") + "\n")
            # copy files from project root to build location
            if "required_files" in config["build"]:
                for file in config["build"]["required_files"]:
                    (workdir / file["dest"]).mkdir(exist_ok=True, parents=True)
                    copy(Path(".config") / file["file"], Path(workdir / file["dest"]))
                    if file.get("secret"):
                        secret_files.append(Path(workdir / file["dest"] / file["file"]))

            if "commands" in config["build"]:
                for command in config["build"]["commands"]:
                    br = TestResult(test_type="build", cmd=command)
                    command = shlex.split(command)
                    br.retval, br.stdout, br.stderr = utils.run_command(
                        command, cwd=workdir
                    )
                    logfile.write(br.log(config["output"]["build"]))

        # loop through and run all tests
        test_runner = TestRunner(logfile, workdir, config)
        test_runner.run_all()
        test_runner.log()

        for file in secret_files:
            file.unlink()


if __name__ == "__main__":
    cli()
