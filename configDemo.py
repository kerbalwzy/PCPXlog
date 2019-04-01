class ConfigDemo:
    class Basic:
        LEVEL = "INFO"
        FORMAT = "[%(levelname)s] %(asctime)s <%(name)s> %(pathname)s line:%(lineno)d :%(message)s"

    class Console:
        LEVEL = "INFO"
        FORMAT = "[%(levelname)s] %(asctime)s <%(name)s> %(pathname)s line:%(lineno)d :%(message)s"

    class File:
        # TYPE = "Ordinary" or "Rotating"
        TYPE = "Rotating"
        FILE_PATH = "./logs/log"
        MAX_BYTES = 5
        BACKUP_COUNT = 3

    class Mongodb:
        pass
