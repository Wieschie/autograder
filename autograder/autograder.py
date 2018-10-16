"""
Command line utility to launch automatic grading of programming assignments
"""

import click
from datetime import datetime
import shlex
from shutil import copyfile
import toml
from utils import *



def junit():
    """ runs junit against specified directory """


@click.command()
# @click.option("--directory", prompt="Directory to test", help="Directory to test")
def proof_of_concept():
    """ Hardcoded method that builds and tests all sample projects """
    directory = "/home/wieschie/Documents/senior_design/sample_projects"
    lib_dir = Path(directory) / ".lib"
    logfile_name = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + ".log"
    for subdir in walk_subdirs(directory):
        print(f"========== Testing {subdir.stem} ==========")
        # make output directory for compilation
        outdir = subdir / "out/p05"
        outdir.mkdir(exist_ok=True, parents=True)
        copyfile(str(lib_dir / "ComplexTests.class"), str(subdir / "out/p05/ComplexTests.class"))

        with open(str(subdir / logfile_name), "w") as logfile:
            logfile.write(box_text("Build Step"))
            compile_cmd = shlex.split(f'''javac -cp "{lib_dir}/*:{subdir / "src"}" -d {subdir / "out"} ''' +
                                      "src/p05/Complex.java src/p05/EX13_17.java")
            ret, out, err = run_command(compile_cmd, subdir)
            logfile.write(" ".join(compile_cmd) + "\n")
            log_command(logfile, ret, out, err)

            logfile.write(box_text("Unit Tests"))
            test_cmd = shlex.split(f'''java -jar {lib_dir}/junit-platform-console-standalone-1.3.1.jar -cp ''' +
                                   f'''"{subdir / "out"}"  -c p05.ComplexTests --reports-dir={subdir / "out"} ''' +
                                   "--disable-ansi-colors")
            ret, out, err = run_command(test_cmd, subdir)
            logfile.write(" ".join(test_cmd) + "\n")
            log_command(logfile, ret, out, err)

            logfile.write(box_text("Diff 1"))
            diff_cmd = ["java", "p05.EX13_17"]
            re, out, err = run_command(diff_cmd,  subdir / "out", "1 1 2 2")
            logfile.write(" ".join(diff_cmd) + "\n")
            logfile.write(f"\nCommand exited with value {ret}\n")
            with open(lib_dir / "output.txt") as f:
                logfile.write("Diff output:\n")
                logfile.write(diff_output(f, out))


def dispatch():
    """ parse config file and run build and tests accordingly """
    with open("config.toml", "r") as f:
        config = toml.load(f)
    lib_dir = Path(".lib")
    logfile_name = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + ".log"
    for sub in walk_subdirs("."):
        (sub / "out/p05").mkdir(exist_ok=True, parents=True)
        try:
            # copy files from .lib to build location
            if "required_files" in config["build"]:
                for file in config["build"]["required_files"]:
                    file["dest"] = file["dest"].replace("<student>", str(sub))
                    copyfile(str(lib_dir / file["file"]), file["dest"])
            # TODO build and compilation steps here
        except KeyError as error:
            print("Missing required key in config file.")
            print(error)


if __name__ == "__main__":
    proof_of_concept()
