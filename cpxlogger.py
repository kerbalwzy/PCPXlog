"""
----------------------------------
CPXLogger Config Handler Support |
----------------------------------
Present:                         |
    console                      |
    file                         |
    rotating_file                |
----------------------------------
Future:                          |
    mongodb                      |
    mysql                        |
    redis                        |
----------------------------------
"""
import logging
import json
from configLoader import ConfigLoader

_ConfigAlreadyLoadErrorInfo = """Log configuration has been loaded, do not load configuration again.
If you are sure you want to reload the configuration, call 'CPXLogger.clean_config()' first,
to clear the original configuration information."""


class CPXLogger:
    default_level = logging.DEBUG
    default_format = '[%(levelname)s] %(asctime)s <%(name)s> %(pathname)s line:%(lineno)d :%(message)s'

    __logger = None
    __config_tag = False
    __handlers = list()
    __config_dict = dict()

    @classmethod
    def __create_handler(cls, handler_class, init_params, log_level, format_str):
        """
        Create a log handler and add it into cls.__handlers
        :param handler_class: the log handler class
        :param init_params: the init params for create this handler object
        :param log_level: the log level for this handler
        :param format_str: the log output format for this handler
        :return: None
        """
        new_handler = handler_class(**init_params)
        new_handler.setLevel(log_level)
        new_formatter = logging.Formatter(format_str)
        new_handler.setFormatter(new_formatter)
        cls.__handlers.append(new_handler)

    @classmethod
    def __create_logger(cls, name: str):
        """
        Create the logger and add the handlers
        :param name: logger name
        :return: None
        """
        logging.basicConfig(level=cls.default_level, format=cls.default_format)
        cls.__logger = logging.getLogger(name)
        for handler in cls.__handlers:
            cls.__logger.addHandler(handler)

    @classmethod
    def __load_config(cls, config: dict):
        """
        Get config information from the config dict.

        The config for console log output is from Basic or Console key-value. if not all of them,
        it will use the default setting. if all of them, the Basic config information will be
        covered with the Console config information.



        :param config: config information dict
        :return: None
        """
        basic_cnf = config.get("Basic", None)
        if basic_cnf:
            cls.default_level = getattr(logging, basic_cnf.get("LEVEL", "DEBUG"))
            cls.default_format = basic_cnf.get("FORMAT", cls.default_format)
            del config["Basic"]

        console_cnf = config.get("Console", None)
        if console_cnf:
            cls.default_level = getattr(logging, console_cnf.get("LEVEL", "DEBUG"))
            cls.default_format = console_cnf.get("FORMAT", cls.default_format)
            del config["Console"]

        # deal the config for file log output
        file_log_cnf = config.get("File", None)
        if file_log_cnf:
            # get file log handler create params
            params = ConfigLoader.load_file_config(config=file_log_cnf)
            # create handler
            cls.__create_handler(**params)
            del config["File"]

        # TODO deal the config for mongodb log output
        pass

    @classmethod
    def config_from_dict(cls, config_dict: dict) -> None:
        """
        Load the config from a dict
        :param config_dict: the config dcit
        :return: None
        """
        assert not cls.__config_tag, _ConfigAlreadyLoadErrorInfo
        cls.__load_config(config_dict)
        cls.__config_tag = True

    @classmethod
    def config_from_class(cls, config_class: object) -> None:
        """
        Load the log config from a class object
        :param config_class: the class object
        :return: None
        """
        assert not cls.__config_tag, _ConfigAlreadyLoadErrorInfo

        # Translate the configClass to a configDict
        config_dict = dict()
        subclass_names = (name for name in dir(config_class) if name.isalpha() and name[0].isupper())
        for name in subclass_names:
            sub_class = getattr(config_class, name)
            config_detail = {attr: getattr(sub_class, attr)
                             for attr in dir(sub_class) if attr.isupper()}
            config_dict.update({name: config_detail})
        cls.__load_config(config_dict)
        cls.__config_tag = True

    @classmethod
    def config_from_file(cls, config_file: str, encoding=None) -> None:
        """
        Load the log config from a json file
        :param config_file:  the path of the file
        :param encoding: the coding type of the file
        :return: None
        """
        assert not cls.__config_tag, _ConfigAlreadyLoadErrorInfo

        with open(config_file, "r", encoding=encoding) as f:
            config_dict = json.loads(f.read(), encoding=encoding)
        cls.__load_config(config_dict)
        cls.__config_tag = True

    @classmethod
    def clean_config(cls):
        # clean all about of the log config
        cls.__config_tag = False
        cls.__handlers.clear()
        cls.__config_dict.clear()
        cls.__logger = None

    @staticmethod
    def create_logger(name="CPXLogger"):
        """
        :param name:
        :return:
        """
        if not CPXLogger.__logger:
            CPXLogger.__create_logger(name)
        return CPXLogger.__logger
