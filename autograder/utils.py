"""
Utility functions for autograder
"""


import difflib
from pathlib import Path
import subprocess as sp
import sys
from typing import List, TextIO

# timeout of commands in seconds
TIMEOUT = 10


def box_text(text: str) -> str:
    """
    Draws an Unicode box around the original content

    Args:
        text: original content (should be 80 characters or less)

    Returns:
        A four-line string.  Unicode box with content centered and a newline at the end.
    """
    top = "┌" + '─' * (len(text) + 2) + '┐'
    bot = '└' + '─' * (len(text) + 2) + '┘'
    return top + "\n│ " + text + " │\n" + bot + "\n"


def diff_output(expected: TextIO, actual: str) -> str:
    """
    Compares the expected and actual outputs of a command

    Args:
        expected: text file containing expected output
        actual: STDOUT captured from command

    Returns:
        str: diff output
    """
    # process expected file
    expected = expected.readlines()
    # expected = [l.strip() for l in expected]

    return ''.join(difflib.unified_diff(expected, actual.splitlines(True), fromfile="expected", tofile="actual"))


def log_command(file: TextIO, ret: int, out: str, err: str):
    """ Writes output of command to a specified file """
    file.write(f"\nCommand exited with value {ret}\n")
    file.write("STDOUT:\n")
    file.write(out + "\n")
    file.write("STDERR:\n")
    file.write(err)


def print_command(ret: int, out: str, err: str):
    log_command(sys.stdout, ret, out, err)


def run_command(cmd: List[str], cwd: Path = None, sinput: str = None) -> (int, str, str):
    """
    Runs a given command, saving output

    Args:
        cmd: Command and arguments to run
        cwd: Working directory to use
        sinput: text input to pipe to process

    Returns:
        - return value of process, or -1 if timed out
        - STDOUT of process
        - STDERR of process
    """
    proc = sp.Popen(cmd, cwd=cwd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    try:
        if sinput is not None:
            sinput = sinput.encode('utf-8')
        out, err = proc.communicate(sinput, timeout=TIMEOUT)
        return_value = proc.wait()
    except sp.TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
        return_value = -1
    return return_value, out.decode(), err.decode()


def walk_subdirs(directory: str) -> List[Path]:
    """ does a flat walk of directory and returns all visible subdirectories """
    subdirectories = []
    for entry in Path(directory).iterdir():
        # ignore hidden directories (like .git)
        if entry.is_dir() and entry.name[0] != '.':
            subdirectories.append(entry)
    return subdirectories
