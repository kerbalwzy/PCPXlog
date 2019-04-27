# defaultConfig.py 
# saved an class config demo and a dict config deme


class CPXLogConfigDemo:
    """
    Using a class object to save config information.

    Basic : is a global setting for the 'LEVEL' and 'FORMAT'. if in an other Handler config class,
        for example, in Console did not defined 'FORMAT', it will use from Basic.

    Console: setting for output log information on terminate.

    File: setting for write log information in file. The 'TYPE' has two choice, 'Ordinary' or 'Rotating'.
        'Ordinary' meanings to use 'FileHandler' from logging module, and only need to set 'FILE_PATH'.
        'Rotating' meanings to use 'RotatingFileHandler' from logging.handlers module, and need set more.
    """

    class Basic:
        """
        the global log 'LEVEL' and 'FORMAT' setting, if there an other Handler config class not set
        about this two option, it will use from here.
        """
        LEVEL = "DEBUG"
        FORMAT = "[%(levelname)s] %(asctime)s <%(name)s> %(pathname)s line:%(lineno)d :%(message)s"

    class Console:
        LEVEL = "DEBUG"
        FORMAT = "[%(levelname)s] %(asctime)s <%(name)s> %(pathname)s line:%(lineno)d :%(message)s"

    class File(Basic):
        TYPE = "Rotating"
        FILE_PATH = "./logs/log"
        MAX_BYTES = 1024
        BACKUP_COUNT = 3

    class Mongodb:
        pass


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
