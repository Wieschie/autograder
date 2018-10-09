"""
Command line utility to launch automatic grading of programming assignments
"""

import click
from pathlib import Path
import shlex
import subprocess as sp
from typing import List


# timeout of commands in seconds
TIMEOUT = 1


@click.command()
@click.option("--directory", prompt="Directory to test", help="Directory to test")
def junit(directory):
    """ runs junit against specified directory """
    for sub in walk_subdirs(directory):
        # make output directory for compilation
        (sub / "out").mkdir(exist_ok=True)
        compile_cmd = shlex.split(f"""javac -cp "lib/*:{sub / "src"}" -d {sub / "out"} {sub / "src/p05"}""")
        test_cmd = shlex.split(f"""java -jar lib/junit-platform-console-standalone-1.3.1.jar -cp "{sub / "out"}"  -c p05.ComplexTests --reports-dir={sub / "out"}""")

    # cmd = ["ping", directory]
    # ret, out, err = run_command(cmd)
    # print("\nOUTPUT: \n")
    # print(out)


def run_command(cmd: List[str]) -> (int, str, str):
    """
    Runs a given command, saving output

    Args:
        cmd: Command and arguments to run

    Returns:
        - return value of process, or -1 if timed out
        - STDOUT of process
        - STDERR of process
    """
    proc = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    out, err = "", ""
    try:
        out, err = proc.communicate(timeout=TIMEOUT)
        return_value = proc.wait()
    except sp.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        return_value = -1
        print(f"Command `{proc.args[0]}` timed out.")
    return return_value, out.decode(), err.decode()


def walk_subdirs(directory: str) -> List[Path]:
    """ does a flat walk of directory and returns all visible subdirectories """
    subdirectories = []
    for entry in Path(directory).iterdir():
        # ignore hidden directories (like .git)
        if entry.is_dir() and entry.name[0] != '.':
            subdirectories.append(entry)
    return subdirectories


if __name__ == "__main__":
    junit()
