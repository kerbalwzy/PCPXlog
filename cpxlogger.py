import logging
from logging import handlers
import json
import contants
from pprint import pprint

_ConfigAlreadyLoadErrorInfo = "Log配置已经加载过了, 请勿重复加载配置。\n" \
                              "如果你确定要重新加载配置，请先调用 CPXLogger.clean_config() 来清空原来的配置信息\n"
_SupportHandlers = ["Console", "File", "RotatingFile", "Mongodb"]


class CPXLogger:
    __default_level = logging.DEBUG
    __default_format = '[%(levelname)s] %(asctime)s <%(name)s> %(pathname)s line:%(lineno)d :%(message)s'

    __logger = None
    __config_tag = False
    __handlers = list()
    __config_dict = dict()

    @classmethod
    def __create_handler(cls, HandlerClass, init_params, log_level, format_str):
        new_handler = HandlerClass(**init_params)
        new_handler.setLevel(log_level)
        new_formatter = logging.Formatter(format_str)
        new_handler.setFormatter(new_formatter)
        cls.__handlers.append(new_handler)

    def __add_handlers(self):
        pass

    def __create_logger(self, name):
        logging.basicConfig(level=self.__default_level, format=self.__default_format)
        self.__logger = logging.getLogger(name)

    @classmethod
    def __load_config(cls, config: dict):
        print("RAW CONFIG:")
        pprint(config)

        Basic = config.get("Basic", None)
        if Basic:
            cls.__default_level = getattr(logging, Basic.get("LEVEL", "DEBUG"))
            cls.__default_format = Basic.get("FORMAT", cls.__default_format)

            del config["Basic"]

        Console = config.get("Console", None)
        if Console:
            cls.__default_level = getattr(logging, Console.get("LEVEL", "DEBUG"))
            cls.__default_format = Console.get("FORMAT", cls.__default_format)
            del config["Console"]

        File = config.get("File", None)
        if File:
            # get FileHandlerClass and the config information
            file_log_type = File.get("TYPE", "Ordinary")
            handler_class = logging.FileHandler
            handler_init_params = dict(
                filename=File["FILE_PATH"],
                encoding=File.get("ENCODING", None),
                delay=File.get("DELAY", False)
            )
            if file_log_type == "Rotating":
                handler_class = handlers.RotatingFileHandler
                handler_init_params["maxBytes"] = File["MAX_BYTES"]
                handler_init_params["backupCount"] = int(File["BACKUP_COUNT"])

            log_level = getattr(logging, File.get("LEVEL", None)) if File.get("LEVEL", None) else cls.__default_level
            format_str = File.get("FORMAT", cls.__default_format)

            # create handler
            cls.__create_handler(HandlerClass=handler_class,
                                 init_params=handler_init_params,
                                 log_level=log_level,
                                 format_str=format_str)

    @classmethod
    def config_from_dict(cls, config_dict: dict) -> None:
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
    def config_from_file(cls, config_file, encoding=None) -> None:
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
            CPXLogger().__create_logger(name)
        return CPXLogger.__logger
