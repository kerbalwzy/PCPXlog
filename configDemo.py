# saved config demo

"""
ConfigDictDemo = {
    'Basic': {
        'FORMAT': '[%(levelname)s] %(asctime)s <%(name)s> %(pathname)s line:%(lineno)d :%(message)s',
        'LEVEL': 'DEBUG'
    },
    'Console': {
        'FORMAT': '[%(levelname)s] %(asctime)s <%(name)s> %(pathname)s line:%(lineno)d :%(message)s',
        'LEVEL': 'DEBUG'
    },

    'File': {
        'BACKUP_COUNT': 3,
        'FILE_PATH': './logs/log',
        'MAX_BYTES': 1024,
        'TYPE': 'Rotating'
    },
    'Mongodb': {}
}
"""


class CPXLogConfigDemo:
    """
    Using a class object to save config information.
    Every sub class saved a config for one type of log handler, and it reduces duplicate code by inheritance.
    """

    class Basic:
        """
        the global log 'LEVEL' and 'FORMAT' setting, if there an other Handler config class not set
        about this two option, it will use from here.
        """
        LEVEL = "INFO"
        FORMAT = "[%(levelname)s] %(asctime)s <%(name)s> %(pathname)s line:%(lineno)d :%(message)s"

    class Console(Basic):
        # Console: setting for output log information on terminate.
        LEVEL = "DEBUG"

    class File(Basic):
        """
        File: Settings for write log information in file. The 'TYPE' has two choice, 'Ordinary' or 'Rotating'.
        'Ordinary' meanings to use 'FileHandler' from logging module, and only need to set 'FILE_PATH'.
        'Rotating' meanings to use 'RotatingFileHandler' from logging.handlers module, and need set more.
        """
        TYPE = "Rotating"
        FILE_PATH = "./logs/log"
        MAX_BYTES = 1024
        BACKUP_COUNT = 3

    class Mongodb(Basic):
        """
        Mongodb: Settings for save log information into mongodb. The log handler will be used is create by
        this project, 'RotatingMongodbHandler'. Actually，every init params for this handler have default
        value.
        """
        HOST = "127.0.0.1"
        PORT = 27017
        USER = None
        PASSWORD = None
        # DB is the database name
        DB = "CPXLog"
        # COLL_NAME is the basic name for collections
        COLL_NAME = "logs"
        # the COLL_SIZE and COLL_COUNT is recommended to use default values
