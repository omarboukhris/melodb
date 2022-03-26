
from loggers import ILogger


class Order:

	def __init__(self, order: dict, logger: ILogger = ILogger("Order_DataClass")):
		self.logger = logger
		if logger is None:
			self.logger = ILogger("Order_DataClass")

		assert order.keys() == Order.labels, self.logger.error("Ill formed order dictionary")

		self.order_id = order["order_id"]
		self.status = order["status"]
		self.symbol = order["symbol"]
		self.instrument = order["instrument"]
		self.order_type = order["type"]
		self.side = order["side"]
		self.price = order["price"]
		self.quantity = order["quantity"]
		self.open_ts = order["open_ts"]
		self.close_ts = order["close_ts"]

	@staticmethod
	def labels():
		return [
			"order_id",
			"status",      # Open/Closed
			"symbol",      # EURUSD ...
			"instrument",  # CFD, OPT, FUT
			"type",        # LMT, MKT
			"side",        # BUY, SELL
			"price",
			"quantity",
			"open_ts",     # timestamp
			"close_ts"
		]

