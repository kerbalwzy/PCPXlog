"""
----------------------------------
CPXLogger Config Handler Support |
----------------------------------
Present:                         |
    console                      |
    file                         |
    rotating_file                |
    mongodb                      |
----------------------------------
Future:                          |
    mysql                        |
    redis                        |
    ....                         |
----------------------------------
"""
import logging
import json

from pcpxlog.cpxUtils import CheckAnnotation


class CPXLogger:
    default_level = logging.DEBUG
    default_format = '[%(levelname)s] %(asctime)s <%(name)s> %(pathname)s line:%(lineno)d :%(message)s'

    __logger = None
    handlers = list()
    __loaded_config = False

    @classmethod
    def __create_handler(cls, handler_class, init_params, log_level, format_str):
        # Create a log handler and add it into cls.handlers

        new_handler = handler_class(**init_params)

        new_handler.setLevel(log_level)
        new_formatter = logging.Formatter(format_str)
        new_handler.setFormatter(new_formatter)

        cls.handlers.append(new_handler)

    @classmethod
    @CheckAnnotation.check_params
    def __create_logger(cls, name: str):
        # Create the logger and add the handlers

        assert cls.__loaded_config, Exception("You cant not create logger before load config")

        logging.basicConfig(level=cls.default_level, format=cls.default_format)
        cls.__logger = logging.getLogger(name)

        for handler in cls.handlers:
            cls.__logger.addHandler(handler)

    @classmethod
    @CheckAnnotation.check_params
    def __load_config(cls, config: dict):
        """
        Get config information from the config dict.

        The config for console log output is from Basic or Console key-value. if not all of them,
        it will use the default setting. if all of them, the Basic config information will be
        covered with the Console config information.

        The config for other handlers will be processed by ConfigLoader

        :param config: config information dict
        """
        from pcpxlog.cpxLoader import ConfigLoader

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

        # process the config for file log output
        file_log_cnf = config.get("File", None)
        if file_log_cnf:
            # Get file log handler creating params
            params = ConfigLoader.load_file_config(config=file_log_cnf)
            # Create handler
            cls.__create_handler(**params)
            del config["File"]

        # TODO deal the config for mongodb log output
        mongodb_log_cnf = config.get("Mongodb", None)
        if mongodb_log_cnf:
            # Get mongodb handler creating params
            params = ConfigLoader.load_mongodb_config(config=mongodb_log_cnf)
            cls.__create_handler(**params)
            del config["Mongodb"]

    @classmethod
    @CheckAnnotation.check_params
    def config_from_dict(cls, config_dict: dict) -> None:
        # Load the config from a dict

        cls.__clean_config()

        cls.__load_config(config_dict)

        cls.__loaded_config = True

    @classmethod
    @CheckAnnotation.check_params
    def config_from_class(cls, config_class: object) -> None:
        # Load the log config from a class object

        cls.__clean_config()

        # Translate the configClass to a configDict
        config_dict = dict()
        subclass_names = (name for name in dir(config_class) if name.isalpha() and name[0].isupper())
        for name in subclass_names:
            sub_class = getattr(config_class, name)
            config_detail = {attr: getattr(sub_class, attr)
                             for attr in dir(sub_class) if attr.isupper()}
            config_dict.update({name: config_detail})

        cls.__load_config(config_dict)

        cls.__loaded_config = True

    @classmethod
    @CheckAnnotation.check_params
    def config_from_file(cls, config_file_path: str, encoding=None) -> None:
        # Load the log config from a json file

        cls.__clean_config()

        with open(config_file_path, "r", encoding=encoding) as f:
            config_dict = json.loads(f.read(), encoding=encoding)

        cls.__load_config(config_dict)

        cls.__loaded_config = True

    @classmethod
    def __clean_config(cls):
        # clean all about of the log config
        cls.handlers.clear()
        cls.__loaded_config = False
        cls.__logger = None

    @staticmethod
    def create_logger(name="CPXLogger"):
        """
        :param name:
        :return: logger
        """
        if not CPXLogger.__logger:
            CPXLogger.__create_logger(name)
        return CPXLogger.__logger
