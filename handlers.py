import logging
import re
import time
from pprint import pprint

import bson
from bson import ObjectId
from pymongo import MongoClient
from platform import python_version

PYTHON_VERSION = float(python_version()[0:3])

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
                ...
            ],
            newest_log_coll: {
                name: <coll_name>_<create_time_stamp>,
                current_size: 1024 * 1024 * N,
                is_fall: False,
            }

         }
        """
        pass

    def __format_record(self, record):
        """
        Add some attribute for the record object.
        """
        record.message = record.getMessage()

        if self.formatter.usesTime():
            record.asctime = self.formatter.formatTime(record, self.formatter.datefmt)

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatter.formatException(record.exc_info)

        return record

    def parse_log(self, record):
        """
        Translate the record object into a log information dict
        :param record: the log record object
        :return: log_information_dict: the log info dict
        """
        # Get the raw format string and trans record to a dict
        raw_fmt_str = self.formatter._fmt
        record2dict = record.__dict__

        # Create a new dict to save the log information we need
        log_information_dict = dict(_id=ObjectId())
        for key in record2dict:
            if key in raw_fmt_str:
                log_information_dict[key] = record2dict.get(key)

        # Try to save some very important additional information
        exec_text = record2dict.get("exc_text")
        if exec_text:
            log_information_dict['exc_text'] = exec_text
        stack_info = record2dict.get("stack_info")
        if stack_info:
            log_information_dict['stack_info'] = stack_info

        return log_information_dict

    def emit(self, record):
        """
        Get information from record and make it to a dict, then save to mongodb
        """

        record = self.__format_record(record)
        log_data = self.parse_log(record)
        pprint(log_data)

    def close(self):
        """
        Close the connect with mongodb
        """
        print("close")
        self.client.close()


if __name__ == '__main__':
    monodb_log = RotatingMongodbHandler(host="104.128.87.146")
    monodb_log.db_record()
