import anyconfig
import toml


class Config:
    """
    Handles interaction with TOML configuration.
    """

    def __init__(self, filename: str, schema: str):
        """
        Loads and parses config from file.
        Throws `jsonschema.ValidationError` on invalid config file.
        """
        self.__config_dict = dict()
        self.__load_config(filename)
        self.__validate_config(schema)

    def __contains__(self, item):
        return item in self.__config_dict

    def __getitem__(self, item):
        return self.__config_dict[item]

    def __load_config(self, filename):
        """ Loads a .toml config file """
        self.__config_dict = toml.load(filename)

    def __validate_config(self, schema: str):
        """ Validates config using a json schema """
        schema = anyconfig.load(schema)
        anyconfig.validate(self.__config_dict, schema, ac_schema_safe=False)

    def get(self, key):
        return self.__config_dict.get(key)
