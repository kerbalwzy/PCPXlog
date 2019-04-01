import logging
import json

defaultFormat = '[%(levelname)s] %(asctime)s <%(name)s> %(pathname)s line:%(lineno)d :%(message)s'

ConfigAlreadyLoadErrorInfo = "Log配置已经加载过了, 请勿重复加载配置。\n" \
                             "如果你确定要重新加载配置，请先调用 CPXLogger.clean_config() 来清空原来的配置信息\n"


class CPXLogger:
    __logger = None
    __config_tag = False
    __handler_flag = list()
    __config_dict = dict()

    def __create_logger(self, name):
        pass

    @classmethod
    def __load_config(cls, config_dict):
        cls.__handler_flag.extend(config_dict.keys())

    @classmethod
    def config_from_dict(cls, config_dict: dict) -> None:
        assert cls.__config_tag, ConfigAlreadyLoadErrorInfo
        cls.__load_config(config_dict)

    @classmethod
    def config_from_class(cls, config_class: object) -> None:
        assert cls.__config_tag, ConfigAlreadyLoadErrorInfo

    @classmethod
    def config_from_file(cls, config_file, encoding=None) -> None:
        """
        从文件加载配置信息
        :param config_file: 配置文件路径
        :param encoding: 文件编码方式
        :return: None
        """
        assert cls.__config_tag, ConfigAlreadyLoadErrorInfo
        with open(config_file, "r", encoding=encoding) as f:
            config_dict = json.loads(f.read(), encoding=encoding)
        cls.__load_config(config_dict)
        cls.__config_tag = True

    @classmethod
    def clean_config(cls):
        cls.__config_tag = False
        cls.__handler_flag = list()
        cls.__config_dict = dict()
        cls.__logger = None

    @staticmethod
    def create_logger(name):
        if not CPXLogger.__logger:
            CPXLogger().__create_logger(name)
        return CPXLogger.__logger
