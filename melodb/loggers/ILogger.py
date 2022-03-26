
class ILogger:
	def __init__(self, component: str):
		self.component = component

	def info(self, log_message: str):
		pass

	def warn(self, log_message: str):
		pass

	def error(self, log_message: str):
		pass

	def err(self, log_message: str):
		self.error(log_message)
