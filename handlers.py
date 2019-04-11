import logging
from pymongo import MongoClient
from platform import python_version

PYTHON_VERSION = float(python_version()[0:3])

DB_EXIST_ERROR = "You have turn on the database check and the database %s already exist. If you are sure, " \
                 "please make param reuse=True"
COLL_EXIST_ERROR = "You have turn on the collection check and the collection %s already exist. If you are sure," \
                   " please make param reuse=True"

# the max size of single collection is 16MB.
# So we set the MONGODB_COLL_MAX_SIZE = 15MB to keep safe
MONGODB_COLL_MAX_SIZE = 1024 * 1024 * 15
# the max count of collection in a databases is 12000
# So we set the MONGODB_COLL_MAX_COUNT = 11000 to keep safe
MONGODB_COLL_MAX_COUNT = 11000


class RotatingMongodbHandler(logging.Handler):

    def __init__(self, host="127.0.0.1", port=27017, user=None, password=None,
                 db="CPXLog", coll_name="logs", coll_size=MONGODB_COLL_MAX_SIZE,
                 coll_count=MONGODB_COLL_MAX_COUNT):

        """
        Get a collection operator to save log information. And the default database name will be 'CPXLog'，
        the default collection name will be 'logs'. The max size of single collection allow be 15MB, and
        the max count of the log collection in a database allow be 11K. If the space of the 'logs' collection
        is empty, it will create a new collection also named 'logs', and the old one will be renamed as a
        time interval.

        :param host: the host of mongodb server
        :param port: the port of mongodb server
        :param user: the username for auth
        :param password: the password for auth
        :param db: the database name for save all log collections
        :param coll_name: the collection name for save logs information
        :param coll_size: the max size of single log collection
        :param coll_count: the count of the log collection in the database
        """
        logging.Handler.__init__(self)

        # create mongodb client
        if user or password:
            uri = 'mongodb://' + user + ':' + password + '@' + host + ':' + str(port) + '/'
        else:
            uri = 'mongodb://' + host + ':' + str(port) + '/'
        self.client = MongoClient(uri)
        self.db = self.client[db]
        self.base_coll_name = coll_name
        self.coll_size = coll_size
        self.coll_count = coll_count
        self.__RotatingMongodbLogRecordName = "RotatingMongodbLogRecord"

    def emit(self, record):
        print("log for mongodb========================")
        print(record)
        print("log for mongodb========================")

    def close(self):
        """
        Close the connect with mongodb
        """
        self.client.close()
