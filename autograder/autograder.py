"""
Command line utility to launch automatic grading of programming assignments
"""

import click
from datetime import datetime
import shlex
from shutil import copyfile

from Config import Config
from TestRunner import TestRunner
from utils import *


@click.command()
# @click.option("--directory", prompt="Directory to test", help="Directory to test")
def proof_of_concept():
    """ Hardcoded method that builds and tests all sample projects """
    directory = "/home/wieschie/Documents/senior_design/sample_projects"
    libdir = Path(directory) / ".lib"
    logfile_name = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + ".log"
    for subdir in walk_subdirs(directory):
        print(f"========== Testing {subdir.stem} ==========")
        # make output directory for compilation
        outdir = subdir / "out" / "p05"
        outdir.mkdir(exist_ok=True, parents=True)

        copyfile(str(libdir / "ComplexTests.class"), str(subdir / "out/p05/ComplexTests.class"))

        with open(str(subdir / logfile_name), "w") as logfile:
            logfile.write(box_text("Build Step"))
            compile_cmd = shlex.split(f'''javac -cp "{libdir}/*:{subdir / "src"}" -d {outdir} ''' +
                                      "src/p05/Complex.java src/p05/EX13_17.java")
            ret, out, err = run_command(compile_cmd, cwd=subdir)
            logfile.write(" ".join(compile_cmd) + "\n")
            log_command(logfile, ret, out, err)

            logfile.write(box_text("Unit Tests"))
            test_cmd = shlex.split(f'''java -jar {libdir}/junit-platform-console-standalone-1.3.1.jar -cp ''' +
                                   f'''"{outdir}"  -c p05.ComplexTests --reports-dir={subdir / "out"} ''' +
                                   "--disable-ansi-colors")
            ret, out, err = run_command(test_cmd, cwd=subdir)
            logfile.write(" ".join(test_cmd) + "\n")
            log_command(logfile, ret, out, err)

            logfile.write(box_text("Diff 1"))
            diff_cmd = ["java", "p05.EX13_17"]
            re, out, err = run_command(diff_cmd, cwd=(subdir / "out"), sinput="1 1 2 2")
            logfile.write(" ".join(diff_cmd) + "\n")
            logfile.write(f"\nCommand exited with value {ret}\n")
            with open(libdir / "output.txt") as f:
                logfile.write("Diff output:\n")
                logfile.write(diff_output(f, out))


def dispatch():
    """ parse config file and run build and tests accordingly """

    config = Config()
    libdir = Path(".lib")
    logfile_name = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + ".log"

    # loop through all subdirectories (project submissions)
    for workdir in walk_subdirs("."):
        config.replace(workdir)
        (workdir / config["output_dir"]).mkdir(exist_ok=True, parents=True)
        with open(str(workdir / logfile_name), "w") as logfile:
            if "build" in config:
                logfile.write(box_text("Build Step"))
                # copy files from project root to build location
                if "required_files" in config["build"]:
                    for file in config["build"]["required_files"]:
                        Path(Path(file["dest"]).absolute().parent).mkdir(exist_ok=True, parents=True)
                        copyfile(str(libdir / file["file"]), file["dest"])

                if "commands" in config["build"]:
                    for command in config["build"]["commands"]:
                        command = shlex.split(command)
                        ret, out, err = run_command(command, cwd=workdir)
                        logfile.write(" ".join(command) + "\n")
                        log_command(logfile, ret, out, err)

            # loop through and run all tests
            test_runner = TestRunner(logfile, libdir, workdir, workdir / config["output_dir"], config["test"])
            test_runner.run_all()


if __name__ == "__main__":
    # proof_of_concept()
    dispatch()
