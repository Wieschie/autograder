"""
Handles actual execution of defined tests.
"""


import shlex
from typing import Dict

from TestResult import TestResult, DiffTestResult
from utils import *


class TestRunner:

    def __init__(self, logfile: TextIO, libdir: Path, workdir: Path, outdir: Path, tests: List):
        self.logfile: TextIO = logfile
        self.libdir: Path = libdir
        self.workdir: Path = workdir
        self.outdir: Path = outdir
        self.tests: List = tests
        self.results: List[TestResult] = []

    def run_all(self):
        for t in self.tests:
            if t["type"] == "junit":
                self.__junit_test(t)
            elif t["type"] == "diff":
                self.__diff_test(t)
            else:
                raise KeyError(f"Unrecognized test type {t['type']}")

    def log(self):
        for tr in self.results:
            self.logfile.write(str(tr))

    def __junit_test(self, test: Dict):
        """ runs junit test file """
        tr = TestResult(test["name"])
        cmd = shlex.split(f'''java -jar {self.libdir}/junit-platform-console-standalone-1.3.1.jar -cp ''' +
                          f'''"{self.outdir}"  -c {test["classname"]} --reports-dir={self.outdir} ''' +
                          "--disable-ansi-colors")
        tr.ret, tr.stdout, tr.stderr = run_command(cmd, cwd=self.workdir)
        tr.cmd = " ".join(cmd) + "\n"
        self.results.append(tr)

    def __diff_test(self, test: Dict):
        """ runs a specified command and compares the result to the expected output  """
        tr = DiffTestResult(test["name"])
        tr.cmd = test["command"]
        cmd = shlex.split(tr.cmd)
        tr.ret, tr.stdout, tr.stderr = run_command(cmd, cwd=(self.workdir / "out"), sinput=test["input"],
                                                   timeout=test.get("timeout"))
        with open(str(self.libdir / test["expected"])) as f:
            tr.diffout = diff_output(f, tr.stdout)
        self.results.append(tr)
