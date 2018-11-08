"""
Command line utility to launch automatic grading of programming assignments
"""

import shlex
import click
from datetime import datetime
from jsonschema import ValidationError
from shutil import copyfile

from Config import Config
from TestResult import TestResult
from TestRunner import TestRunner
from utils import *


@click.group()
def cli():
    pass


@cli.command()
def genconfig():
    """ Generate a skeleton config directory """
    try:
        (Path(".") / ".config").mkdir()
    except FileExistsError:
        raise click.UsageError(".config directory already exists.")
    copyfile(str(libdir() / "config.toml"), Path(".") / ".config")


@cli.command()
def runall():
    """ Build and test all projects """
    try:
        config = Config(
            ".config/config.toml", str((libdir() / "config_schema.json").absolute())
        )
    except FileNotFoundError:
        print("No config file found.  Are you in the root directory of a project?")
        exit(1)
    except ValidationError as e:
        print(f"Invalid config file:\n{e.message}")
        exit(1)

    logfile_name = datetime.now().strftime("autograder_%Y-%m-%dT%H-%M-%S") + ".log"

    # loop through all subdirectories (project submissions)
    for workdir in walk_subdirs("."):
        print(f"========== Grading {workdir.stem} ==========")

        (workdir / config["output_dir"]).mkdir(exist_ok=True, parents=True)
        with (workdir / logfile_name).open("w", encoding="utf-8") as logfile:
            if "build" in config:
                logfile.write(box_text("Build Step") + "\n")
                # copy files from project root to build location
                if "required_files" in config["build"]:
                    for file in config["build"]["required_files"]:
                        (workdir / file["dest"]).mkdir(exist_ok=True, parents=True)
                        copyfile(
                            Path(".config") / file["file"],
                            Path(workdir / file["dest"] / file["file"]),
                        )

                if "commands" in config["build"]:
                    for command in config["build"]["commands"]:
                        br = TestResult(cmd=command)
                        command = shlex.split(command)
                        br.ret, br.stdout, br.stderr = run_command(command, cwd=workdir)
                        logfile.write(str(br))

            # loop through and run all tests
            test_runner = TestRunner(
                logfile,
                workdir,
                config["output_dir"],
                config["test"],
                config.get("memory_limit"),
                config.get("process_limit"),
            )
            test_runner.run_all()
            test_runner.log()


if __name__ == "__main__":
    cli()
