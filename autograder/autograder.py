"""
Command line utility to launch automatic grading of programming assignments
"""

import click
from pathlib import Path
import shlex
from shutil import copyfile
from utils import *


@click.command()
@click.option("--directory", prompt="Directory to test", help="Directory to test")
def junit(directory):
    """ runs junit against specified directory """
    directory = "/home/wieschie/Documents/senior_design/sample_projects"
    lib_dir = Path(directory) / ".lib"
    for sub in walk_subdirs(directory):
        print(f"========== Testing {sub.stem} ==========")
        # make output directory for compilation
        (sub / "out/p05").mkdir(exist_ok=True, parents=True)
        copyfile(lib_dir / "ComplexTests.class", sub / "out/p05/ComplexTests.class")
        compile_cmd = shlex.split(f'''javac -cp "{lib_dir}/*:{sub / "src"}" -d {sub / "out"} ''' +
                                  "src/p05/Complex.java src/p05/EX13_17.java")
        test_cmd = shlex.split(f'''java -jar {lib_dir}/junit-platform-console-standalone-1.3.1.jar -cp ''' +
                               f'''"{sub / "out"}"  -c p05.ComplexTests --reports-dir={sub / "out"}''')
        print(compile_cmd)
        print(test_cmd)
        ret, out, err = run_command(compile_cmd, sub)
        print_command(ret, out, err)
        ret, out, err = run_command(test_cmd, sub)
        print_command(ret, out, err)


if __name__ == "__main__":
    junit()
