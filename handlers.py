import logging
from pymongo import MongoClient
from platform import python_version

PYTHON_VERSION = float(python_version()[0:3])

DB_EXIST_ERROR = "The database %s already exist. If you are sure, please make param reuse=True"
COLL_EXIST_ERROR = "The collection %s already exist. If you are sure, please make param reuse=True"


class MongodbHandler(logging.Handler):

    def __init__(self, host="127.0.0.1", port=27017,
                 user=None, password=None, db="CPXLog", coll=None,
                 db_validate=False, coll_validate=False, reuse=False):
        """

        :param host:
        :param port:
        :param db:
        :param col:
        """
        logging.Handler.__init__(self)

        # create mongodb client and check if need to validate db

        if user or password:
            uri = 'mongodb://' + user + ':' + password + '@' + host + ':' + str(port) + '/'
        else:
            uri = 'mongodb://' + host + ':' + str(port) + '/'

        client = MongoClient(uri)
        if db_validate:
            db_list = client.list_database_names() if float(PYTHON_VERSION) >= 3.7 else client.database_names()
            assert (db in db_list and not reuse), DB_EXIST_ERROR % db
        log_db = client[db]
        if coll_validate:
            coll_list = log_db.list_collection_names() if float(PYTHON_VERSION) >= 3.7 else log_db.collection_names()
            assert (coll in coll_list and not reuse), COLL_EXIST_ERROR % coll
        log_coll = log_db[coll]

    def emit(self, record):
        print("log for mongodb========================")
        print(record)
        print("log for mongodb========================")

    def close(self):
        """
        Close the connect with mongodb
        """
        pass
