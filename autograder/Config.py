import toml
from pathlib import Path


class Config:

    def __init__(self):
        self._config_str = ""
        self._config_dict = dict()
        self._load_config()

    def __getitem__(self, item):
        return self._config_dict[item]

    def replace(self, working_directory: Path):
        """ replace placeholder values """
        tmp = self._config_str.replace("<student>", str(working_directory))
        self._config_dict = toml.loads(tmp)

    def _load_config(self):
        """ loads config.toml from working directory and attempts to validate it with some simple rules"""
        try:
            with open("config.toml", "r") as f:
                self._config_str = f.read()
                self._config_dict = toml.loads(self._config_str)
                self._validate_config(self._config_dict)
        except FileNotFoundError:
            print("No config file found.  Are you in the root directory of a project?")
            exit(1)

    @staticmethod
    def _validate_config(config: dict):
        if "output_dir" not in config:
            raise KeyError("output_dir missing in config.toml")

        if "build" in config:
            if "required_files" in config["build"]:
                for file in config["build"]["required_files"]:
                    for key in ["file", "dest"]:
                        if key not in file:
                            raise KeyError(key + " missing from required_files in config.toml")

        if "test" not in config:
            raise KeyError("No tests defined in config.toml")

        for t in config["test"]:
            for key in ["name", "type"]:
                if key not in t:
                    raise KeyError(key + " missing from test definition in config.toml")

            if t["type"] == "junit":
                if "classname" not in t:
                    raise KeyError("classname missing from junit test definition in config.toml")

            elif t["type"] == "diff":
                for key in ["command", "input", "expected"]:
                    if key not in t:
                        raise KeyError(key + " missing from diff test definition in config.toml")
            else:
                raise KeyError("Unrecognized test type in config.toml")
