
from melodb.loggers import ILogger, ConsoleLogger, MongoLogger
from typing import List

class CompositeLogger(ILogger):

	def __init__(self, loggers: List[ILogger]):
		super(CompositeLogger, self).__init__("")
		self.loggers = loggers

	@staticmethod
	def build_composite_logger(
		component_name: str,
		dburl: str = "mongodb://localhost:27017/"):

		return CompositeLogger([
			ConsoleLogger(component_name),
			MongoLogger(component_name, dburl)
		])

	def info(self, log_message: str):
		for logger in self.loggers:
			logger.info(log_message)

	def warn(self, log_message: str):
		for logger in self.loggers:
			logger.warn(log_message)

	def error(self, log_message: str):
		for logger in self.loggers:
			logger.error(log_message)

