from utils import box_text


class TestResult:
    """
    Holds results of test execution, and handles formatting in output.
    """

    def __init__(
        self,
        name: str = None,
        cmd: str = None,
        ret: int = None,
        stdout: str = None,
        stderr: str = None,
        points: float = None,
        maxpoints: float = None,
    ):
        self.name = name
        self.cmd = cmd
        self.ret = ret
        self.stdout = stdout
        self.stderr = stderr
        self.points = points
        self.maxpoints = maxpoints

    def __str__(self):
        name = f"{box_text(self.name)}\n" if self.name else ""
        s = f"{name}Points awarded: {self.points} of {self.maxpoints}\n`{self.cmd}`\nExited with code {self.ret}\n"
        if len(self.stdout) > 0:
            s += f"STDOUT:\n{self.stdout}\n"
        if len(self.stderr) > 0:
            s += f"STDERR:\n{self.stderr}\n"
        return s

    @staticmethod
    def csv_header() -> str:
        return f"name, points, maxpoints"

    def to_csv(self) -> str:
        return f"{self.name},{self.points},{self.maxpoints}"


class DiffTestResult(TestResult):
    def __init__(
        self,
        name: str = None,
        cmd: str = None,
        ret: int = None,
        stdout: str = None,
        stderr: str = None,
        points: float = None,
        maxpoints: float = None,
        diffout: str = None,
    ):
        TestResult.__init__(self, name, cmd, ret, stdout, stderr, points, maxpoints)
        self.diffout = diffout

    def __str__(self):
        s = TestResult.__str__(self)
        if len(self.diffout) > 0:
            s += f"DIFFOUT:\n{self.diffout}"
        return s
