""""
Handles interaction with config.toml
"""


import anyconfig
from jsonschema import ValidationError
import toml
from pathlib import Path


class Config:

    def __init__(self, filename):
        self.__config_dict = dict()
        self.__load_config(filename)

    def __contains__(self, item):
        return item in self.__config_dict

    def __getitem__(self, item):
        return self.__config_dict[item]

    def __load_config(self, filename):
        """ loads config.toml from working directory and attempts to validate it with some simple rules"""
        try:
            self.__config_dict = toml.load(filename)
        except FileNotFoundError:
            raise FileNotFoundError("No config file found.  Are you in the root directory of a project?")

        self.__validate_config()

    def __validate_config(self):
        schema = anyconfig.load("config_schema.json")
        try:
            anyconfig.validate(self.__config_dict, schema, ac_schema_safe=False)
        except ValidationError as e:
            raise ValidationError(f"Invalid config file:\n{e.message}")

    def get(self, key):
            return self.__config_dict.get(key)

