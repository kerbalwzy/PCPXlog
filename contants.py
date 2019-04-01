
config2handlers_params_map = {
    "LEVEL": "level",
    "FORMAT": "format",
    "FILE_PATH": "filename",
    "ENCODING": "encoding",
    "DELAY": "delay",
    "MAX_BYTES": "maxBytes",
    "BACKUP_COUNT": "backupCount"
}


class BasicConfigMap:
    LEVEL = "LEVEL"
    FORMAT = "FORMAT"


class ConsoleConfigMap(BasicConfigMap):
    pass


class FileConfigMap(BasicConfigMap):
    TYPE = "TYPE"
    FILE_PATH = "FILE_PATH"
    MAX_BYTES = "MAX_BYTES"
    BACKUP_COUNT = "BACKUP_COUNT"


class MongodbConfigMap(BasicConfigMap):
    pass
