import logging
import time
import bson

from pymongo import MongoClient

# the max size of single collection is 16MB.
# So we set the MONGODB_COLL_MAX_SIZE = 15MB to keep safe
MONGODB_COLL_MAX_SIZE = 1024 * 1024 * 15
# the max count of collection in a databases is 12000
# So we set the MONGODB_COLL_MAX_COUNT = 11000 to keep safe
MONGODB_COLL_MAX_COUNT = 11000


class RotatingMongodbHandler(logging.Handler):
    """
    The handler class, helping save log information into mongodb.
    The default name of database will be 'CPXLog' and every collection will be named 'log_<createTime>'.
    The max size of single collection allow be 15MB, and the max count of the log collection in a database
    allow be 11K. If the space of the 'logs_<createTime>' collection is not enough, it will create a new
    collection.So it can store about 161GB log data totally.

    And it will create a collection named 'logSavingState' extra to record log data saving state.
    The structure of the only data saved in the collection is like this:

        {
            _id: ObjectId(<id_auto_created>),
            tag: "CPXLog-mongodb",
            coll_size: <coll_size>,
            coll_remainder_count: <coll_count>,
            history_log_coll: [
                {
                    name: <coll_name>_<create_time_stamp>,
                    current_size: N ( <= coll_size ) ,
                },
                ...
            ],
            current_log_coll: {
                name: <coll_name>_<create_time_stamp>,
                current_size: n ( <= coll_size ),
            }

         }

    """

    def __create_coll(self):
        """
        Set the value for self.__dbStateColl object, and try to init the state of log saving.
        Then set the value for self.__logDataColl object.
        """
        self.__dbStateColl = self.db[self.__stateCollName]

        log_saving_state = self.__dbStateColl.find_one(dict(tag=self.__handlerTag))
        if log_saving_state:
            self.__logsStateID = log_saving_state["_id"]
        else:
            log_saving_state = dict(
                tag=self.__handlerTag,
                coll_size=self.collSize,
                coll_remainder_count=self.collCount - 1,
                history_log_coll=list(),
                current_log_coll=dict(
                    name=self.baseCollName + "_" + str(int(round(time.time()))),
                    current_size=0,
                )
            )
            ret = self.__dbStateColl.insert_one(log_saving_state)
            self.__logsStateID = ret.inserted_id

        # create the current log collection cursor
        self.__logDataColl = self.db[log_saving_state["current_log_coll"]["name"]]

    def __init__(self, host="127.0.0.1", port=27017, user=None, password=None, db="CPXLog", coll_name="logs",
                 coll_size=MONGODB_COLL_MAX_SIZE, coll_count=MONGODB_COLL_MAX_COUNT):
        """
        Connect to mongodb server, create the 'logSavingState' collection and initial the log_saving_state.
        And then create the log collection cursor ready to save log data

        :param db: the database name for save all log collections
        :param coll_name: the collection name for save logs information
        :param coll_size: the max size of single log collection
        :param coll_count: the count of the log collection in the database
        """
        logging.Handler.__init__(self)
        assert 0 < coll_count <= MONGODB_COLL_MAX_COUNT, ValueError("The value out of range for Param coll_count")
        assert 0 < coll_size <= MONGODB_COLL_MAX_SIZE, ValueError("The value out of range for Param coll_size")
        # create mongodb client cursor
        if user or password:
            uri = 'mongodb://' + user + ':' + password + '@' + host + ':' + str(port) + '/'
        else:
            uri = 'mongodb://' + host + ':' + str(port) + '/'
        self.client = MongoClient(uri)

        # create logs database cursor
        self.db = self.client[db]

        # create LogRecord and collection cursor, if no data in this collection then init it.
        self.baseCollName = coll_name
        self.collSize = int(coll_size)
        self.collCount = int(coll_count)

        self.__handlerTag = "CPXLog-mongodb"
        self.__stateCollName = "logSavingState"
        self.__logsStateID = None
        self.__dbStateColl = None
        self.__logDataColl = None

        self.__create_coll()

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
        record = self.__format_record(record)

        # Get the raw format string and trans record to a dict
        raw_fmt_str = self.formatter._fmt
        record2dict = record.__dict__

        # Create a new dict to save the log information we need
        log_information_dict = dict(_id=bson.ObjectId())
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

    def __check_coll_count(self, log_saving_state):
        """
        When the remainder count of the log data collection is zero, The earliest created collection
        will be deleted to store more log data.
        """
        coll_remainder_count = log_saving_state["coll_remainder_count"]

        if coll_remainder_count == 0:
            earliest_log_data_coll_name = log_saving_state["history_log_coll"].pop(0).get('name')
            earliest_log_data_coll = self.db[earliest_log_data_coll_name]
            earliest_log_data_coll.drop()
            log_saving_state["coll_remainder_count"] += 1

        return log_saving_state

    def __check_coll_size(self, log_saving_state, log_data):
        """
        When the remainder size of the current log data collection is not enough, It will move the
        state information of the 'current_log_coll' into 'history_log_coll' creating a dictionary
        to save the state information of new 'current_log_coll'
        """
        coll_size = log_saving_state["current_log_coll"]["current_size"]
        data_size = len(bson.BSON.encode(log_data))
        new_coll_size = coll_size + data_size

        if new_coll_size > self.collSize:
            log_saving_state["coll_remainder_count"] -= 1
            current_log_state = log_saving_state["current_log_coll"]
            log_saving_state["history_log_coll"].append(current_log_state)

            new_log_coll_name = self.baseCollName + "_" + str(int(round(time.time())))
            new_log_state = {"name": new_log_coll_name, "current_size": data_size}
            log_saving_state["current_log_coll"] = new_log_state

        else:
            log_saving_state["current_log_coll"]["current_size"] = new_coll_size

        return log_saving_state

    def __check_saving_state(self, state_query_rule, log_data):
        """
        Get log saving state from 'logSavingState' collection by self.__dbStateColl.
        Then check remainder size of the current log data collection, and check the
        remainder count of the log data collection. After all checked, get a new
        'log_saving_state'
        """
        log_saving_state = self.__dbStateColl.find_one(filter=state_query_rule)

        log_saving_state = self.__check_coll_size(log_saving_state, log_data)

        log_saving_state = self.__check_coll_count(log_saving_state)

        return log_saving_state

    def save(self, log_data):
        """
        Check the state about the log information saving, and record the log collection have
        saved how many data.
        """
        state_query_rule = {"_id": self.__logsStateID}
        log_saving_state = self.__check_saving_state(state_query_rule, log_data)

        self.__logDataColl = self.db[log_saving_state["current_log_coll"]["name"]]
        try:
            # Save log info into mongodb
            self.__logDataColl.insert_one(log_data)
            # Update the saving state info
            self.__dbStateColl.update_one(filter=state_query_rule,
                                          update={'$set': log_saving_state})
        except Exception as e:
            raise e
            # TODO May can send a email to manager in the future

    def emit(self, record):
        """
        Get information from record and make it to a dict, then save into mongodb
        """
        log_data = self.parse_log(record)
        self.save(log_data)

    def close(self):
        """
        Close the connect with mongodb
        """
        self.client.close()


if __name__ == '__main__':
    pass
