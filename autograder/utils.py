"""
Utility functions for autograder
"""

import sys

import difflib
import subprocess as sp
from enum import Enum
from pathlib import Path
from typing import List, TextIO

if "win" in sys.platform:
    from win32_limit import win32_limit
else:
    from .posix_limit import posix_limit


def box_text(text: str) -> str:
    """
    Draws an Unicode box around the original content

    Args:
        text: original content (should be 1 line and 80 characters or less)

    Returns:
        A three-line string.  Unicode box with content centered.
    """
    top = "┌" + "─" * (len(text) + 2) + "┐"
    bot = "└" + "─" * (len(text) + 2) + "┘"
    return top + "\n│ " + text + " │\n" + bot


def diff_output(expected: str, actual: str) -> str:
    """
    Compares the expected and actual outputs of a command

    Args:
        expected: desired output
        actual: STDOUT captured from command

    Returns:
        str: diff output
    """

    # files read in are converted to "universal" newlines so convert captured output too
    actual = actual.replace("\r\n", "\n")
    return "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile="expected",
            tofile="actual",
        )
    )


def libdir() -> Path:
    """ Returns absolute path of .lib directory for data files """
    if getattr(sys, "frozen", False):
        # running inside pyinstaller bundle
        return Path(sys._MEIPASS) / ".lib"
    else:
        return Path(sys.path[0]) / ".lib"


def log_command(file: TextIO, ret: int, out: str, err: str):
    """ Writes output of command to a specified file """
    file.write(f"\nCommand exited with value {ret}\n")
    file.write("STDOUT:\n")
    file.write(out + "\n")
    file.write("STDERR:\n")
    file.write(err)


def print_command(ret: int, out: str, err: str):
    log_command(sys.stdout, ret, out, err)


class RunError(Enum):
    TIMEOUT = -1
    MEMORYOUT = -2
    SIGSEGV = -3
    NOTEXIST = -4
    UNKNOWN = -5


__errors = {sp.TimeoutExpired: RunError.TIMEOUT, MemoryError: RunError.MEMORYOUT}


def run_command(
    cmd: List[str],
    cwd: Path = None,
    sinput: str = None,
    timeout: float = None,
    memory_limit: int = None,
    process_limit: int = None,
) -> (int, str, str):
    """
    Runs a given command, saving output

    Args:
        cmd: Command and arguments to run
        cwd: Working directory to use
        sinput: text input to pipe to process
        timeout: seconds that command is allowed to run before being killed
        memory_limit: max memory in bytes of process
        process_limit: max processes allowed to spawn (1 means that the command may run
            but not spawn any children)

    Returns:
        - return value of process, or a RunError enum if exceptions are raised
        - STDOUT of process
        - STDERR of process
    """

    # set up process limits
    preexec = None
    if memory_limit or process_limit:
        if "win" not in sys.platform:

            def preexec():
                posix_limit(memory_limit, process_limit)

        else:
            win32_limit(memory_limit, process_limit)

    try:
        proc = sp.Popen(
            cmd,
            cwd=cwd,
            stdin=sp.PIPE,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            preexec_fn=preexec,
        )
    except FileNotFoundError:
        return RunError.NOTEXIST, f"Command not found: {cmd}", ""

    try:
        if sinput is not None:
            sinput = sinput.encode("utf-8")
        out, err = proc.communicate(sinput, timeout=timeout)
        return_value = proc.wait()
    except Exception as ex:
        proc.kill()
        out, err = proc.communicate()
        return_value = __errors.get(type(ex), RunError.UNKNOWN)
    if "win" not in sys.platform and return_value in [-6, -11, -127]:
        return_value = RunError.SIGSEGV
    return return_value, out.decode(), err.decode()


def walk_subdirs(directory: str) -> List[Path]:
    """ does a flat walk of directory and returns all visible subdirectories """
    subdirectories = []
    for entry in Path(directory).iterdir():
        # ignore hidden directories (like .git)
        if entry.is_dir() and entry.name[0] != ".":
            subdirectories.append(entry)
    return subdirectories
