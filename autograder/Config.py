from dataclasses import dataclass
import toml
from typing import List


class Config:

    def __init__(self):
        self._config_dict = dict()
        self._output_dir: str = None
        self._build = None
        self._test = []
        self.load_config()

    def load_config(self):
        """ loads config.toml from working directory and attempts to validate it with some simple rules"""
        try:
            with open("config.toml", "r") as f:
                self._config_dict = toml.load(f)
                self.validate_config(self._config_dict)
        except FileNotFoundError:
            print("No config file found.  Are you in the root directory of a project?")
            exit(1)

    def validate_config(self, config: dict):
        if "output_dir" not in config:
            raise KeyError("output_dir missing in config.toml")
        else:
            self._output_dir = config["output_dir"]

        if "build" in config:

            if "required_files" in config["build"]:
                required_files = []
                for file in config["build"]["required_files"]:
                    for key in ["file", "dest"]:
                        if key not in file:
                            raise KeyError(key + " missing from required_files in config.toml")
                    required_files.append(ReqFile(config["build"]["required_files"]["file"],
                                                  config["build"]["required_files"]["dest"]))
                self._build = Build(config["source_dir"], required_files, config["builds"]["commands"])
            else:
                self._build = Build(config["source_dir"], [], config["builds"]["commands"])

        if "test" not in config:
            raise KeyError("No tests defined in config.toml")

        for t in config["test"]:
            for key in ["name", "type"]:
                if key not in t:
                    raise KeyError(key + " missing from test definition in config.toml")

            if t["type"] == "junit":
                if "classname" not in t:
                    raise KeyError("classname missing from junit test definition in config.toml")
                self._test.append(JUnitTest(t["name"], t["type"], t["classname"]))

            elif t["type"] == "diff":
                for key in ["command", "input", "expected"]:
                    if key not in t:
                        raise KeyError(key + " missing from diff test definition in config.toml")
                    self._test.append(DiffTest(t["name"], t["type"], t["command"], t["input"], t["expected"]))
            else:
                raise KeyError("Unrecognized test type in config.toml")


@dataclass
class Build:
    source_dir: str
    required_files: List
    commands: List[str]


@dataclass
class ReqFile:
    file: str
    dest: str


@dataclass
class Test:
    name: str
    type: str


@dataclass
class JUnitTest(Test):
    classname: str


@dataclass
class DiffTest(Test):
    command: str
    input: str
    expected: str
