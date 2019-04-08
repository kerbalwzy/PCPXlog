import logging
from logging import handlers
from cpxlogger import CPXLogger


class ConfigLoader:
    """
    Be in charge of processing the config for log handlers with out console.
    """
    __cpx_logger = CPXLogger

    @classmethod
    def load_file_config(cls, config: dict):
        """
        if the TYPE is 'Ordinary',the Handler Class will be logging.FileHandler,
        if is 'Rotating', the Handler Class will be logging.handlers.RotatingFileHandler.
        :param config: file log configs
        :return: params : the params for create a file log handler
        """

        file_log_type = config.get("TYPE", "Ordinary")
        handler_class = logging.FileHandler
        handler_init_params = dict(
            filename=config["FILE_PATH"],
            encoding=config.get("ENCODING", None),
            delay=config.get("DELAY", False)
        )
        if file_log_type == "Rotating":
            handler_class = handlers.RotatingFileHandler
            handler_init_params["maxBytes"] = config["MAX_BYTES"]
            handler_init_params["backupCount"] = int(config["BACKUP_COUNT"])

        log_level_str = config.get("LEVEL", None)
        log_level = getattr(logging, log_level_str) if log_level_str else cls.__cpx_logger.default_level

        format_str = config.get("FORMAT", cls.__cpx_logger.default_format)

        params = dict(handler_class=handler_class,
                      init_params=handler_init_params,
                      log_level=log_level,
                      format_str=format_str)
        return params
