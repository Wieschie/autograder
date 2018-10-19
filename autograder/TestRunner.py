"""
Handles actual execution of defined tests.
"""


import shlex
from typing import Dict

from utils import *


class TestRunner:

    def __init__(self, logfile: TextIO, libdir: Path, workdir: Path, outdir: Path, tests: List):
        self.logfile: TextIO = logfile
        self.libdir: Path = libdir
        self.workdir: Path = workdir
        self.outdir: Path = outdir
        self.tests: List = tests

    def run_all(self):
        for t in self.tests:
            self.logfile.write(box_text(t["name"]))
            if t["type"] == "junit":
                self.__junit_test(t)
            elif t["type"] == "diff":
                self.__diff_test(t)
            else:
                raise KeyError(f"Unrecognized test type {t['type']}")

    def __junit_test(self, test: Dict):
        """ runs junit test file """
        cmd = shlex.split(f'''java -jar {self.libdir}/junit-platform-console-standalone-1.3.1.jar -cp ''' +
                          f'''"{self.outdir}"  -c {test["classname"]} --reports-dir={self.outdir} ''' +
                          "--disable-ansi-colors")
        ret, out, err = run_command(cmd, cwd=self.workdir)
        self.logfile.write(" ".join(cmd) + "\n")
        log_command(self.logfile, ret, out, err)

    def __diff_test(self, test: Dict):
        """ runs a specified command and compares the result to the expected output  """
        cmd = test["command"]
        cmd = shlex.split(cmd)
        ret, out, err = run_command(cmd, cwd=(self.workdir / "out"), sinput=test["input"])
        self.logfile.write(" ".join(cmd) + "\n")
        log_command(self.logfile, ret, out, err)
        # self.logfile.write(f"\nCommand exited with value {ret}\n")
        with open(str(self.libdir / test["expected"])) as f:
            self.logfile.write("Diff output:\n")
            self.logfile.write(diff_output(f, out))
