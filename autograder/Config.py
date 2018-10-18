import anyconfig
import toml
from pathlib import Path


class Config:

    def __init__(self):
        self._config_str = ""
        self._config_dict = dict()
        self._load_config()

    def __contains__(self, item):
        return item in self._config_dict

    def __getitem__(self, item):
        return self._config_dict[item]

    def replace(self, student_dir: Path):
        """ replace placeholder values """
        tmp = self._config_str.replace("<student>", str(student_dir))
        self._config_dict = toml.loads(tmp)

    def _load_config(self):
        """ loads config.toml from working directory and attempts to validate it with some simple rules"""
        try:
            with open("config.toml", "r") as f:
                self._config_str = f.read()
                self._config_dict = toml.loads(self._config_str)
                self._validate_config()
        except FileNotFoundError:
            print("No config file found.  Are you in the root directory of a project?")
            exit(1)

    def _validate_config(self):
        if "output_dir" not in self._config_dict:
            raise KeyError("output_dir missing in config.toml")

        if "build" in self._config_dict:
            if "required_files" in self._config_dict["build"]:
                for file in self._config_dict["build"]["required_files"]:
                    for key in ["file", "dest"]:
                        if key not in file:
                            raise KeyError(key + " missing from required_files in config.toml")

        if "test" not in self._config_dict:
            raise KeyError("No tests defined in config.toml")

        for t in self._config_dict["test"]:
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

            # check against schema at the end: more precise, but no helpful errors
            schema = anyconfig.load("config_schema.json")
            anyconfig.validate(self._config_dict, schema, ac_schema_safe=False)

