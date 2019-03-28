import logging
import json

defaultFormat = '[%(levelname)s] %(asctime)s <%(name)s> %(pathname)s line:%(lineno)d :%(message)s'


class CPXLogger:

    def __init__(self):
        pass

    def config_from_dict(self, config_dict: dict) -> None:
        pass

    def config_from_class(self, config_class: object) -> None:
        pass

    def config_from_file(self, config_file) -> None:
        pass

    def create_logger(self) -> logging.Logger:
        pass
