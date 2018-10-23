"""
Command line utility to launch automatic grading of programming assignments
"""

import shlex
from datetime import datetime
from jsonschema import ValidationError
from shutil import copyfile

from Config import Config
from TestResult import TestResult
from TestRunner import TestRunner
from utils import *


def dispatch():
    """ parse config file and run build and tests accordingly """
    try:
        config = Config("config.toml")
    except (FileNotFoundError, ValidationError) as e:
        print(e.message)
        exit(1)

    libdir = Path(".lib").absolute()
    logfile_name = datetime.now().strftime("autograder_%Y-%m-%dT%H:%M:%S") + ".log"

    # loop through all subdirectories (project submissions)
    for workdir in walk_subdirs("."):
        print(f"========== Grading {workdir.stem} ==========")

        (workdir / config["output_dir"]).mkdir(exist_ok=True, parents=True)
        with open(str(workdir / logfile_name), "w") as logfile:
            if "build" in config:
                logfile.write(box_text("Build Step") + "\n")
                # copy files from project root to build location
                if "required_files" in config["build"]:
                    for file in config["build"]["required_files"]:
                        (workdir / file["dest"]).mkdir(exist_ok=True, parents=True)
                        copyfile(libdir / file["file"], Path(workdir / file["dest"] / file["file"]))

                if "commands" in config["build"]:
                    for command in config["build"]["commands"]:
                        br = TestResult(cmd=command)
                        command = shlex.split(command)
                        br.ret, br.stdout, br.stderr = run_command(command, cwd=workdir)
                        logfile.write(str(br))

            # loop through and run all tests
            test_runner = TestRunner(logfile, libdir, workdir, config["output_dir"], config["test"])
            test_runner.run_all()
            test_runner.log()


if __name__ == "__main__":
    dispatch()
