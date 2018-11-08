import shlex

from TestResult import TestResult, DiffTestResult
from utils import *


class TestRunner:
    """
    Handles actual execution of defined tests.
    """

    def __init__(
        self,
        logfile: TextIO,
        workdir: Path,
        outdir: Path,
        tests: List,
        memory_limit: int = None,
        process_limit: int = None,
    ):
        self.logfile: TextIO = logfile
        self.workdir: Path = workdir
        self.outdir: Path = outdir
        self.tests: List = tests  #: list of tests directly from config dictionary
        self.memory_limit = memory_limit
        self.process_limit = process_limit
        self.results: List[TestResult] = []

    def run_all(self):
        """ Runs all defined tests, and stores output in `results[]` """
        for t in self.tests:
            if t["type"] == "junit":
                self.__junit_test(t)
            elif t["type"] == "diff":
                self.__diff_test(t)
            else:
                raise KeyError(f"Unrecognized test type {t['type']}")

    def log(self):
        """ Writes full results to logfile """
        for tr in self.results:
            self.logfile.write(str(tr))

    def __junit_test(self, test):
        """ Runs a junit test .class file """
        tr = TestResult(test["name"])
        cmd = shlex.split(
            f"""java -jar {libdir() / "junit-platform-console-standalone-1.3.1.jar"} -cp """
            f""""{self.outdir}"  -c {test["classname"]} --reports-dir={self.outdir} """
            "--disable-ansi-colors",
            posix=("win" not in sys.platform),
        )
        tr.ret, tr.stdout, tr.stderr = run_command(cmd, cwd=self.workdir)
        tr.cmd = " ".join(cmd)
        self.results.append(tr)

    def __diff_test(self, test):
        """ Runs a specified command and compares the result to the expected output  """
        tr = DiffTestResult(test["name"])
        tr.cmd = test["command"]
        cmd = shlex.split(tr.cmd)
        tr.ret, tr.stdout, tr.stderr = run_command(
            cmd,
            cwd=(self.workdir / "out"),
            sinput=test["input"],
            timeout=test.get("timeout"),
            memory_limit=self.memory_limit,
            process_limit=self.process_limit,
        )
        with (Path(".config") / test["expected"]).open() as f:
            tr.diffout = diff_output(f, tr.stdout)
        self.results.append(tr)
