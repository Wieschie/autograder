"""
Command line utility to launch automatic grading of programming assignments
"""

import click
import subprocess as sp
from typing import List

# timeout of commands in seconds
TIMEOUT = 10


@click.command()
@click.option("--directory", prompt="Directory to test", help="Directory to test")
def junit(directory):
    """runs junit against specified directory"""
    cmd = ["ping", directory]
    ret, out, err = run_command(cmd)
    print("\nOUTPUT: \n")
    print(out)


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


if __name__ == "__main__":
    junit()
