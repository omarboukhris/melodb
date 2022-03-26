
from loggers import ILogger

class Order:

	def __init__(self, logger: ILogger = ILogger("Order_DataClass"), **order):
		self.logger = logger
		if logger is None:
			self.logger = ILogger("Order_DataClass")

		assert order.keys() == Order.labels, self.logger.error("Ill formed order dictionary")

		self.order_id = order["order_id"]
		self.status = order["status"]
		self.symbol = order["symbol"]
		self.instrument = order["instrument"]
		self.order_type = order["order_type"]
		self.side = order["side"]
		self.price = order["price"]
		self.quantity = order["quantity"]
		self.open_ts = order["open_ts"]
		self.close_ts = order["close_ts"]
		self.forecast = order["forecast"]

	@staticmethod
	def empty():
		return Order(
			order_id=0,
			status="open",
			symbol="",
			instrument="",
			order_type="",
			side="",
			price=0.,
			quantity=0,
			open_ts="",
			close_ts="",
			forecast=0.
		)

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

	def to_dict(self):
		return {
			"order_id": self.order_id,
			"status": self.status,
			"symbol": self.symbol,
			"instrument": self.instrument,
			"type": self.order_type,
			"side": self.side,
			"price": self.price,
			"quantity": self.quantity,
			"open_ts": self.open_ts,
			"close_ts": self.close_ts
		}

