import logging

from bson import ObjectId
from pymongo import MongoClient
from platform import python_version
import time

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
        assert 0 < coll_count <= MONGODB_COLL_MAX_COUNT, "The value out of range for Param coll_count"
        assert 0 < coll_size <= MONGODB_COLL_MAX_SIZE, "The value out of range for Param coll_size"
        # create mongodb client cursor
        if user or password:
            uri = 'mongodb://' + user + ':' + password + '@' + host + ':' + str(port) + '/'
        else:
            uri = 'mongodb://' + host + ':' + str(port) + '/'
        self.client = MongoClient(uri)

        # create logs database cursor
        self.db = self.client[db]
        self.base_coll_name = coll_name
        self.coll_size = int(coll_size)
        self.coll_count = int(coll_count)

        # create LogRecord collection cursor, if no data in this collection then init it.
        self.__logs_record_id = None
        self.__Handler_tag = "CPXLog-mongodb"
        self.__RecordColl = self.db["LogRecord"]

        current_record = self.__RecordColl.find_one(dict(tag=self.__Handler_tag))
        if current_record:
            self.__logs_record_id = current_record["_id"]
        else:
            current_record = dict(
                tag=self.__Handler_tag,
                coll_size=self.coll_size,
                coll_count=self.coll_count,
                history_log_coll=list(),
                current_log_coll=dict(
                    name=self.base_coll_name + "_" + str(int(round(time.time()))),
                    current_size=0,
                    is_fall=False
                )
            )
            ret = self.__RecordColl.insert_one(current_record)
            self.__logs_record_id = ret.inserted_id

        # create the current log collection cursor
        self.current_log_coll = self.db[current_record["current_log_coll"]["name"]]

    def db_record(self):
        """
        Check the status about the log information saving, and record the log collection have
        saved how many data.
        The logs record data structure example:
        {
            _id: ObjectId(<id_auto_created_by_mongodb>),
            tag: "CPXLog-mongodb",
            coll_size: <coll_size>,
            coll_count: <coll_count>,
            coll_details: [
                {
                    name: <coll_name>_<create_time_stamp>,
                    current_size: <coll_size>,
                    is_fall: True,
                },
                {
                    name: <coll_name>_<create_time_stamp>,
                    current_size: <coll_size>,
                    is_fall: True,
                },
                ......
            ],
            newest_log_coll: {
                name: <coll_name>_<create_time_stamp>,
                current_size: 1024 * 1024 * N,
                is_fall: False,
            }

         }
        """
        # history_record = self.__RecordColl.find_one(dict(_id=self.__logs_record_id))
        import bson
        # data_size = bson.BSON.encode(history_record)
        # print(data_size)
        # status = self.__RecordColl.stats()
        # print(status)
        test_date = dict(_id=ObjectId(), name="laowang")
        bson_test_data = bson.BSON.encode(test_date)
        print("raw length:", len(bson_test_data))
        ret = self.current_log_coll.insert_one(test_date)
        print(ret.inserted_id)
        get_test_date = self.current_log_coll.find_one(dict(_id=test_date["_id"]))
        print("get length:", len(bson.BSON.encode(get_test_date)))
        pass

    def emit(self, record):
        print("log for mongodb========================")
        print(record)
        print("log for mongodb========================")

    def close(self):
        """
        Close the connect with mongodb
        """
        self.client.close()


if __name__ == '__main__':
    monodb_log = RotatingMongodbHandler(host="104.128.87.146")
    monodb_log.db_record()
