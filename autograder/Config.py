""""
Handles interaction with config.toml
"""


import anyconfig
from jsonschema import ValidationError
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
            schema = anyconfig.load("config_schema.json")
            try:
                anyconfig.validate(self._config_dict, schema, ac_schema_safe=False)
            except ValidationError as e:
                print(f"Invalid config file:\n{e.message}")
                exit(1)

