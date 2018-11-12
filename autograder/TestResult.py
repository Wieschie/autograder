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

    def log(self):
        name = f"{box_text(self.name)}\n" if self.name else ""
        points = (
            f"Points awarded: {self.points:1g} of {self.maxpoints:1g}\n"
            if self.maxpoints
            else ""
        )
        out = f"STDOUT:\n{self.stdout}\n" if len(self.stdout) > 0 else ""
        err = f"STDERR:\n{self.stderr}\n" if len(self.stderr) > 0 else ""
        s = (
            f"{name}{points}Command `{self.cmd}` exited with code {self.ret}\n"
            f"{out}{err}"
        )
        return s

    @staticmethod
    def csv_header() -> str:
        return f"name, points, maxpoints"

    def to_csv(self) -> str:
        return f"{self.name},{self.points},{self.maxpoints}"


class DiffTestResult(TestResult):
    def __init__(self, diffout: str = None, **kwargs):
        super().__init__(**kwargs)
        self.diffout = diffout

    def log(self):
        s = super().log()
        if len(self.diffout) > 0:
            s += f"DIFFOUT:\n{self.diffout}"
        return s
