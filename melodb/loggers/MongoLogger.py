
from melodb.loggers.ILogger import ILogger
from datetime import datetime
import pymongo

class MongoLogger(ILogger):
	def __init__(
		self,
		component: str,
		dburl: str = "mongodb://localhost:27017/"
	):
		super(MongoLogger, self).__init__(component)

		self.dburl = dburl
		self.mongo_client = None
		self.db_connection = None
		self.connected = False

		self.connect()

	def connect(self):
		self.mongo_client = pymongo.MongoClient(self.dburl)
		self.db_connection = self.mongo_client["melo-db"]
		self.connected = True

	def close(self):
		self.mongo_client = None
		self.db_connection = None
		self.connected = False

	def _write_mongo_log(self, log_dict: dict):
		log_collection = self.db_connection["logs"]
		log_collection.insert_one(log_dict)

	def _read_mongo_log(self, log_dict_request: dict, limit: int = 10):
		if limit > 10:
			limit = 10
		if limit < 1:
			limit = 10
		log_collection = self.db_connection["logs"]
		return log_collection\
			.find(log_dict_request, {})\
			.sort("date", pymongo.ASCENDING)\
			.limit(limit)

	def info(self, log_message: str):
		log_dict = {
			"type": "INFO",
			"date": datetime.now(),
			"component": self.component,
			"message": log_message
		}
		self._write_mongo_log(log_dict)

	def warn(self, log_message: str):
		log_dict = {
			"type": "WARN",
			"date": datetime.now(),
			"component": self.component,
			"message": log_message
		}
		self._write_mongo_log(log_dict)

	def error(self, log_message: str):
		log_dict = {
			"type": "ERROR",
			"date": datetime.now(),
			"component": self.component,
			"message": log_message
		}
		self._write_mongo_log(log_dict)

	def get_last_logs(self, nb_logs: int = 10):
		return self._read_mongo_log({}, nb_logs)


if __name__ == "__main__":
	mongoLoggger = MongoLogger("mglogger-test")

	for log in mongoLoggger.get_last_logs(nb_logs=5):
		print(log)

