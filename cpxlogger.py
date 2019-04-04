import logging
import json
import contants
from pprint import pprint

__ConfigAlreadyLoadErrorInfo = "Log配置已经加载过了, 请勿重复加载配置。\n" \
                             "如果你确定要重新加载配置，请先调用 CPXLogger.clean_config() 来清空原来的配置信息\n"
__SupportHanlers = ["Console", "File", "RotatingFile","Mongodb"]

class CPXLogger:
    __default_level = logging.DEBUG
    __default_format = '[%(levelname)s] %(asctime)s <%(name)s> %(pathname)s line:%(lineno)d :%(message)s'

    __logger = None
    __config_tag = False
    __handler_flag = list()
    __config_dict = dict()

    def __create_handlers(self, name, init_params):
        pass

    def __add_handlers(self):
        pass

    def __create_logger(self, name):
        logging.basicConfig(level=self.__default_level, format=self.__default_format)
        self.__logger = logging.getLogger(name)

    @classmethod
    def __load_config(cls):
        cls.__handler_flag.extend(cls.__config_dict.keys())


    @classmethod
    def config_from_dict(cls, config_dict: di ct) -> None:
        assert not cls.__config_tag, __ConfigAlreadyLoadErrorInfo
        cls.__config_dict = config_dict
        cls.__config_tag = True

    @classmethod
    def config_from_class( cls, config_class: object) -> None:
        """
        Load the log config from a class object
        :param config_class: the class object
        :return: None
        """
        assert not cls.__config_tag, __ConfigAlreadyLoadErrorInfo

        # Translate the configClass to a configDict
        subclass_names = (name for name in dir(config_class) if name.isalpha() and name[0].isupper())
        for name in subclass_names:
            sub_class = getattr(config_class, name)
            config_detail = {attr: getattr(sub_class, attr)
                             for attr in dir(sub_class) if attr.isupper()}
            cls.__config_dict.update({name: config_detail})
        pprint(cls.__config_dict)
        cls.__config_tag = True

    @classmethod
    def config_from_file(cls, config_file, encoding=None) -> None:
        """
        Load the log config from a json file
        :param config_file:  the path of the file
        :param encoding: the coding type of the file
        :return: None
        """
        assert not cls.__config_tag, __ConfigAlreadyLoadErrorInfo

        with open(config_file, "r", encoding=encoding) as f:
            cls.__config_dict = json.loads(f.read(), encoding=encoding)
        cls.__config_tag = True

    @classmethod
    def clean_config(cls):
        # clean all about of the log config
        cls.__config_tag = False
        cls.__handler_flag.clear()
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
