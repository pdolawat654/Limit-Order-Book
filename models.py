import datetime

order_id = 0
transaction_id = 0
transactions = []
market_bid_orders = []
market_ask_orders = []
limit_bid_orders = []
limit_ask_orders = []

class MarketOrder:
    def __init__(self, size, type):
        global order_id
        order_id += 1
        if type == "ask":
            self.order_id = "MA" + str(order_id)
        if type == "bid":
            self.order_id = "MB" + str(order_id)

        self.size = size
        self.type = type
        self.date = datetime.datetime.now()
        self.time = datetime.datetime.now().timestamp()


class Order:
    def __init__(self, size, type, price):
        global order_id
        order_id += 1
        if type == "ask":
            self.order_id = "LA" + str(order_id)
        if type == "bid":
            self.order_id = "LB" + str(order_id)
        self.time = datetime.datetime.now().timestamp()
        self.size = size
        self.price = price
        self.type = type
        self.date = datetime.datetime.now()

class Transaction:
    def __init__(self, buyers_order_id, sellers_order_id, price, size):
        global transaction_id
        transaction_id += 1
        self.transaction_id = transaction_id
        self.buyers_order_id = buyers_order_id
        self.sellers_order_id = sellers_order_id
        self.price = price
        self.size = size
        transactions.append(self)