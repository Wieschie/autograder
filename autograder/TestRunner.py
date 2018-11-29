import shlex

from Config import Config
import junit
from TestResult import TestResult
from utils import *


class TestRunner:
    """
    Handles actual execution of defined tests.
    """

    def __init__(self, logfile: TextIO, workdir: Path, config: Config):
        self.logfile: TextIO = logfile
        self.workdir: Path = workdir
        self.config = config
        self.outdir: Path = config["output_dir"]
        self.tests: List = config["test"]  #: list of tests directly from config dict
        self.results: List[TestResult] = []

    def log(self):
        """ Writes full results to logfile """
        template_map = {
            "junit": self.config["output"]["junit"],
            "diff": self.config["output"]["diff"],
            "custom": self.config["output"]["custom"],
        }
        points_earned = 0
        max_points = 0
        for tr in self.results:
            if tr.points:
                points_earned += tr.points
                max_points += tr.maxpoints
            self.logfile.write(tr.log(template_map[tr.test_type]))
        self.logfile.write(box_text("Score") + "\n")
        self.logfile.write(f"{points_earned:1g} of {max_points:1g} points earned.")

    def __junit_test(self, test):
        """ Runs a junit test .class file """
        tr = TestResult(name=test["name"], test_type=test["type"])
        junit_runner = "junit-platform-console-standalone-1.3.1.jar"
        cmd = shlex.split(
            (
                f"""java -jar {libdir() / junit_runner}"""
                f""" -cp "{self.outdir}" -c {test["classname"]} --reports-dir="""
                f"""{self.outdir} --disable-ansi-colors"""
            ),
            posix=("win" not in sys.platform),
        )
        tr.retval, tr.stdout, tr.stderr = run_command(cmd, cwd=self.workdir)
        tr.cmd = " ".join(cmd)
        tr.stdout, tr.points, tr.maxpoints = junit.parse_xml(self.workdir / self.outdir)
        self.results.append(tr)

    def __diff_test(self, test):
        """ Runs a specified command and compares the result to the expected output  """
        tr = TestResult(
            name=test["name"],
            test_type=test["type"],
            cmd=test["command"],
            maxpoints=test.get("points"),
        )

        inp = test.get("stdin")
        if inp is None:
            with (Path(".config") / test["stdinFile"]).open() as f:
                inp = f.read()

        out = test.get("stdout")
        if out is None:
            filename = test.get("stdoutFile")
            if filename:
                with (Path(".config") / filename).open() as f:
                    out = f.read()

        err = test.get("stderr")
        if err is None:
            filename = test.get("stderrFile")
            if filename:
                with (Path(".config") / filename).open() as f:
                    err = f.read()

        cmd = shlex.split(tr.cmd)
        tr.retval, tr.stdout, tr.stderr = run_command(
            cmd,
            cwd=(self.workdir / "out"),
            sinput=inp,
            timeout=test.get("timeout"),
            memory_limit=self.config.get("memory_limit"),
            process_limit=self.config.get("process_limit"),
        )

        tr.diffout = ""
        if out:
            tr.diffout += diff_output(out, tr.stdout)
        if err:
            tr.diffout += diff_output(err, tr.stderr)

        # diff is blank if matches perfectly
        if len(tr.diffout) == 0:
            tr.points = tr.maxpoints
            tr.diffout = "Output is identical"
        else:
            tr.points = 0

        self.results.append(tr)

    def __custom_test(self, test):
        """ Runs any arbitrary command and saves output. """
        tr = TestResult(name=test["name"], test_type=test["type"], cmd=test["command"])

        cmd = shlex.split(tr.cmd)
        tr.retval, tr.stdout, tr.stderr = run_command(
            cmd,
            cwd=(self.workdir / "out"),
            sinput="",
            timeout=test.get("timeout"),
            memory_limit=self.config.get("memory_limit"),
            process_limit=self.config.get("process_limit"),
        )

        self.results.append(tr)

    # test type -> test runner mapping
    __test = {"junit": __junit_test, "diff": __diff_test, "custom": __custom_test}

    def run_all(self):
        """ Runs all defined tests, and stores output in `results[]` """
        for t in self.tests:
            try:
                TestRunner.__test[t["type"]](self, t)
            except KeyError as e:
                raise KeyError(f"""Test type {t["type"]} undefined.""")
