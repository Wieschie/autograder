"""
Command line utility to launch automatic grading of programming assignments
"""

import click
from datetime import datetime
import shlex
from shutil import copyfile
from utils import *


@click.command()
# @click.option("--directory", prompt="Directory to test", help="Directory to test")
def junit():
    """ runs junit against specified directory """
    directory = "/home/wieschie/Documents/senior_design/sample_projects"
    lib_dir = Path(directory) / ".lib"
    logfile_name = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + ".log"
    for sub in walk_subdirs(directory):
        print(f"========== Testing {sub.stem} ==========")
        # make output directory for compilation
        (sub / "out/p05").mkdir(exist_ok=True, parents=True)
        copyfile(str(lib_dir / "ComplexTests.class"), str(sub / "out/p05/ComplexTests.class"))

        with open(str(sub / logfile_name), "w") as logfile:
            logfile.write(box_text("Build Step"))
            compile_cmd = shlex.split(f'''javac -cp "{lib_dir}/*:{sub / "src"}" -d {sub / "out"} ''' +
                                      "src/p05/Complex.java src/p05/EX13_17.java")
            ret, out, err = run_command(compile_cmd, sub)
            logfile.write(" ".join(compile_cmd) + "\n")
            log_command(logfile, ret, out, err)

            logfile.write(box_text("Unit Tests"))
            test_cmd = shlex.split(f'''java -jar {lib_dir}/junit-platform-console-standalone-1.3.1.jar -cp ''' +
                                   f'''"{sub / "out"}"  -c p05.ComplexTests --reports-dir={sub / "out"} ''' +
                                   "--disable-ansi-colors")
            ret, out, err = run_command(test_cmd, sub)
            logfile.write(" ".join(test_cmd) + "\n")
            log_command(logfile, ret, out, err)

            logfile.write(box_text("Diff 1"))
            diff_cmd = ["java", "p05.EX13_17"]
            re, out, err = run_command(diff_cmd,  sub / "out", "1 1 2 2")
            logfile.write(" ".join(diff_cmd) + "\n")
            logfile.write(f"\nCommand exited with value {ret}\n")
            with open(lib_dir / "output.txt") as f:
                logfile.write("Diff output:\n")
                logfile.write(diff_output(f, out))


if __name__ == "__main__":
    junit()
