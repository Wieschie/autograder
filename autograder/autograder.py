"""
Command line utility to launch automatic grading of programming assignments
"""

from datetime import datetime
from jsonschema import ValidationError
import shlex
from shutil import copyfile

from Config import Config
from TestRunner import TestRunner
from utils import *


def dispatch():
    """ parse config file and run build and tests accordingly """
    try:
        config = Config()
    except (FileNotFoundError, ValidationError) as e:
        print(e.message)
        exit(1)

    libdir = Path(".lib").absolute()
    logfile_name = datetime.now().strftime("autograder_%Y-%m-%dT%H:%M:%S") + ".log"

    # loop through all subdirectories (project submissions)
    for workdir in walk_subdirs("."):
        (workdir / config["output_dir"]).mkdir(exist_ok=True, parents=True)
        with open(str(workdir / logfile_name), "w") as logfile:
            if "build" in config:
                logfile.write(box_text("Build Step"))
                # copy files from project root to build location
                if "required_files" in config["build"]:
                    for file in config["build"]["required_files"]:
                        (workdir / file["dest"]).mkdir(exist_ok=True, parents=True)
                        copyfile(libdir / file["file"], Path(workdir / file["dest"] / file["file"]))

                if "commands" in config["build"]:
                    for command in config["build"]["commands"]:
                        command = shlex.split(command)
                        ret, out, err = run_command(command, cwd=workdir)
                        logfile.write(" ".join(command) + "\n")
                        log_command(logfile, ret, out, err)

            # loop through and run all tests
            test_runner = TestRunner(logfile, libdir, workdir, config["output_dir"], config["test"])
            test_runner.run_all()


if __name__ == "__main__":
    dispatch()
