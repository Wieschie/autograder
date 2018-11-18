from string import Template
import textwrap

from utils import box_text


class TestResult:
    """
    Holds results of test execution, and handles formatting in output.
    """

    def __init__(
        self,
        test_type: str,
        name: str = None,
        cmd: str = None,
        retval: int = None,
        stdout: str = None,
        stderr: str = None,
        points: float = None,
        maxpoints: float = None,
        diffout: str = None,
    ):
        self.name = name
        self.test_type = test_type
        self.cmd = cmd
        self.retval = retval
        self.stdout = stdout
        self.stderr = stderr
        self.points = points
        self.maxpoints = maxpoints
        self.diffout = diffout if diffout is not None else ""

    def log(self, tmpl: str) -> str:
        """
        Fills out a templated string with log data.

        Args:
            tmpl: Python template string. https://docs.python.org/3/library/string.html#template-strings

        Returns:
            str: full substituted output.  Any invalid identifiers are left as-is

        Notes:
            Valid identifiers:

            * $name
            * $cmd
            * $retval
            * $stdout
            * $stderr
            * $points
            * $diffout
        """
        name = f"{box_text(self.name)}" if self.name else ""
        points = f"{self.points:1g} of {self.maxpoints:1g}" if self.maxpoints else ""

        out = f"STDOUT:\n{self.stdout}" if len(self.stdout) > 0 else ""
        err = f"STDERR:\n{self.stderr}" if len(self.stderr) > 0 else ""
        diff = f"DIFFOUT:\n{self.diffout}" if len(self.diffout) > 0 else ""

        s = Template(tmpl).safe_substitute(
            name=name,
            cmd=textwrap.fill(
                self.cmd, width=88, break_long_words=False, break_on_hyphens=False
            ),
            retval=str(self.retval),
            stdout=out,
            stderr=err,
            points=points,
            diffout=diff,
        )
        return s

    @staticmethod
    def csv_header() -> str:
        return f"name, points, maxpoints"

    def to_csv(self) -> str:
        return f"{self.name},{self.points},{self.maxpoints}"
