
from melodb.loggers import ILogger
from Order import Order
import pymongo
import bson.objectid as boi

class OrderBookManagerMongo:

	component_name = "OrderBookManagerMongo"

	def __init__(self, dburl: str, logger: ILogger = ILogger(component_name)):
		"""
		:param dburl: mongodb url path
		"""

		self.dburl = dburl
		self.mongo_client = None
		self.db_connection = None
		self.connected = False
		self.logger = logger if logger is not None else ILogger(OrderBookManagerMongo.component_name)

	def connect(self):
		self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
		self.db_connection = self.mongo_client["melo-db"]
		self.connected = True

	def close(self):
		self.mongo_client = None
		self.db_connection = None
		self.connected = False

	def create_order_book(self):
		pass

	def queue_order(self, order: Order):
		order_dict = order.to_dict()
		assert set(order_dict.keys()) == set(self.labels()), \
			self.logger.error("Mongo-db insert request not well formed")

		orderbook_collection = self.db_connection["orderbook"]
		query_result = orderbook_collection.insert_one(order_dict)
		self.logger.info(f"Inserted id : {query_result.inserted_id} / order : {order_dict}")

	def update_order(self, order_id: str, order: Order):
		order_dict = order.to_dict()
		assert set(order_dict.keys()) == set(self.labels()), \
			self.logger.error("Mongo-db insert request not well formed")

		query, new_values = {"_id": boi.ObjectId(order_id)}, {"$set": order_dict}
		orderbook_collection = self.db_connection["orderbook"]
		query_result = orderbook_collection.update_one(query, new_values)
		self.logger.info(f"Updated rows count: {query_result.modified_count} / order : {order_dict}")

	def get_order_by_id(self, order_id: str):
		if order_id != "" or order_id is not None:
			return self._select_request({"_id": order_id})

	def get_open_orders(self):
		request = {"status": Order.Status.OPEN}
		return self._select_request(request)

	def get_closed_orders(self):
		request = {"status": Order.Status.CLOSED}
		return self._select_request(request)

	def get_orders(self):
		return self._select_request()

	def delete_by_id(self, order_id: str):
		query = {"_id": boi.ObjectId(order_id)}
		orderbook_collection = self.db_connection["orderbook"]
		query_result = orderbook_collection.delete_one(query)
		self.logger.info(f"Deleted document/row : {query_result.deleted_count} / _id : {order_id}")

	def _apply_request(self, request):
		pass

	def _select_request(self, request: dict = None):
		request = {} if request is None else request
		if not self.connected:
			self.connect()

		orderbook_collection = self.db_connection["orderbook"]
		orders = orderbook_collection.find(request, {})

		if orders is not None:
			self.logger.info("Find request executed. Result is not empty")
		else:
			self.logger.warn("Find request executed. Result is empty")

		return orders

	@staticmethod
	def labels():
		return Order.labels()

	def __del__(self):
		self.close()


if __name__ == "__main__":
	from melodb.loggers import ConsoleLogger, CompositeLogger

	orderbook = OrderBookManagerMongo(
		"mongodb://localhost:27017/",
		CompositeLogger([
			ConsoleLogger(OrderBookManagerMongo.component_name)
		])
	)
	orderbook.connect()

	dummy_order = Order.empty()
	orderbook.queue_order(dummy_order)

	dummy_order.status = Order.Status.OPEN
	orderbook.update_order("623fa650954fb28e8e421455", dummy_order)
	for ordr in orderbook.get_orders():
		print(ordr)

	orderbook.delete_by_id("623fa650954fb28e8e421455")
	for ordr in orderbook.get_orders():
		print(ordr)

	orderbook.close()
