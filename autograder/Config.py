""""
Handles interaction with config.toml
"""


import anyconfig
from jsonschema import ValidationError
import toml
from pathlib import Path


class Config:

    def __init__(self):
        self.__config_str = ""
        self.__config_dict = dict()
        self.__load_config()

    def __contains__(self, item):
        return item in self.__config_dict

    def __getitem__(self, item):
        return self.__config_dict[item]

    def replace(self, student_dir: Path):
        """ replace placeholder values """
        tmp = self.__config_str.replace("<student>", str(student_dir))
        self.__config_dict = toml.loads(tmp)

    def __load_config(self):
        """ loads config.toml from working directory and attempts to validate it with some simple rules"""
        try:
            with open("config.toml", "r") as f:
                self.__config_str = f.read()
                self.__config_dict = toml.loads(self.__config_str)
                self.__validate_config()
        except FileNotFoundError:
            raise FileNotFoundError("No config file found.  Are you in the root directory of a project?")

    def __validate_config(self):
            schema = anyconfig.load("config_schema.json")
            try:
                anyconfig.validate(self.__config_dict, schema, ac_schema_safe=False)
            except ValidationError as e:
                raise ValidationError(f"Invalid config file:\n{e.message}")
