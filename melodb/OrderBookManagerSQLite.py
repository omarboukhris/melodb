
from melodb.loggers import ILogger
from Order import Order
import sqlite3


class OrderBookManagerSQLite:

	component_name = "OrderBookManagerMongo"

	def __init__(self, dbfile: str, logger: ILogger = ILogger(component_name)):
		"""
		:param dbfile: *.db file path
		"""

		self.dbfile = dbfile
		self.db_connection = None
		self.connected = False
		self.logger = logger if logger is not None else ILogger(OrderBookManagerSQLite.component_name)

	def connect(self):
		self.db_connection = sqlite3.connect(self.dbfile)
		self.connected = True

	def close(self):
		self.db_connection.close()
		self.connected = False

	def create_order_book(self):

		labels_str = "order_id STRING NOT NULL PRIMARY KEY, "
		labels_str += ", ".join(OrderBookManagerSQLite.labels()[1:])
		request = f"CREATE TABLE orderbook ({labels_str})"

		self._apply_request(request)

	def queue_order(self, order: dict):
		assert set(order.keys()) == set(self.labels()), \
			self.logger.error("SQLite insert request not well formed")

		orderbook_row = ",".join([f"'{order[label]}'" for label in self.labels()])
		request = f"INSERT INTO orderbook VALUES ({orderbook_row})"
		self._apply_request(request)

	def update_order(self, order_id: str, order: dict):
		assert set(order.keys()) == set(self.labels()), \
			self.logger.error("SQLite update request not well formed")

		orderbook_row = ", ".join([
			f"{label} = '{order[label]}'" for label in self.labels()
		])
		condition = f"order_id = '{order_id}'"
		request = f"UPDATE orderbook SET {orderbook_row} WHERE {condition}"
		self._apply_request(request)

	def get_order_by_id(self, order_id: str):
		request = f"SELECT * FROM orderbook WHERE order_id = 'f{order_id}'"
		return self._select_request(request)

	def get_open_orders(self):
		request = f"SELECT * FROM orderbook WHERE status = 'open'"
		return self._select_request(request)

	def get_closed_orders(self):
		request = f"SELECT * FROM orderbook WHERE status = 'closed'"
		return self._select_request(request)

	def get_orders(self):
		request = f"SELECT * FROM orderbook"
		return self._select_request(request)

	def _apply_request(self, request):
		if not self.connected:
			self.connect()

		try:
			cursor = self.db_connection.cursor()
			cursor.execute(request)
			self.db_connection.commit()
			self.logger.info(f"Request executed [{request}]")
		except Exception as e:
			self.logger.error(f"An exception occured : {e} / request : {request}")

	def _select_request(self, request):
		if not self.connected:
			self.connect()

		output_orders = []
		try:
			cursor = self.db_connection.cursor()
			for order in cursor.execute(request):
				output_orders.append(order)
			self.db_connection.commit()
			self.logger.info(f"Request executed [{request}]")
		except Exception as e:
			self.logger.error(f"An exception occured : {e} / request : {request}")
		finally:
			return output_orders

	@staticmethod
	def labels():
		return Order.labels()

	def __del__(self):
		self.close()


if __name__ == "__main__":
	from melodb.loggers import ConsoleLogger, CompositeLogger

	loggers = CompositeLogger([
		ConsoleLogger(OrderBookManagerSQLite.component_name)
	])

	# orderbook = OrderBookManagerMongo("orderbook-melo.db", loggers)
	# orderbook.connect()
	# orderbook.queue_order(dummy_order)
	# dummy_order["order_id"] = "50"
	# orderbook.update_order("f50-2310", dummy_order)
	# print(orderbook.get_orders())
	# orderbook.close()

	import pymongo

	myclient = pymongo.MongoClient("mongodb://localhost:27017/")

	mydb = myclient["mydatabase"]
	mycol = mydb["orderbook"]

	mydict = {"name": "John", "address": "Highway 37"}

	x = mycol.insert_one(mydict)

	loggers.info(myclient.list_database_names())
	loggers.info(mydb.list_collection_names())

	dblist = myclient.list_database_names()
	if "mydatabase" in dblist:
		loggers.info("The database exists.")

	collist = mydb.list_collection_names()
	if "orderbook" in collist:
		print("The collection exists.")
