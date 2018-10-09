"""
Utility functions for autograder
"""


from pathlib import Path
import subprocess as sp
from typing import List

# timeout of commands in seconds
TIMEOUT = 10


def run_command(cmd: List[str], cwd: str) -> (int, str, str):
    """
    Runs a given command, saving output

    Args:
        cmd: Command and arguments to run
        cwd: Working directory to use

    Returns:
        - return value of process, or -1 if timed out
        - STDOUT of process
        - STDERR of process
    """
    proc = sp.Popen(cmd, cwd=cwd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    out, err = "", ""
    try:
        out, err = proc.communicate(timeout=TIMEOUT)
        return_value = proc.wait()
    except sp.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        return_value = -1
    return return_value, out.decode(), err.decode()


def print_command(ret: int, out: str, err: str):
    print(f"\nCommand exited with value {ret}")
    print("OUTPUT:")
    print(out)
    print("ERRORS:")
    print(err)

def walk_subdirs(directory: str) -> List[Path]:
    """ does a flat walk of directory and returns all visible subdirectories """
    subdirectories = []
    for entry in Path(directory).iterdir():
        # ignore hidden directories (like .git)
        if entry.is_dir() and entry.name[0] != '.':
            subdirectories.append(entry)
    return subdirectories