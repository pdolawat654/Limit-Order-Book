from models import Order, MarketOrder, Transaction, transactions, transaction_id, limit_ask_orders, limit_bid_orders, market_ask_orders, market_bid_orders

# Displays Data for all the tables

def show_data():
    print("\t \t LIMIT ORDERS ")
    print(f'Order ID | Size | Price | Type | Date       | Time')
    if len(limit_ask_orders) > 0:
        count = 0
        for i in limit_ask_orders:
            if count < 5:
                print(f'{i.order_id}        | {i.size}  |{i.price}     | {i.type}  | {i.date.strftime("%d/%m/%Y | %H:%M:%S")}')
                count += 1
            else:
                break
    else:
        print("No ask orders")
    print("---------------------------------------------------------------------------------------")
    print(f'                                Order ID | Size | Price | Type | Date      | Time')
    if len(limit_bid_orders) > 0:
        count = 0
        for i in limit_bid_orders:
            if count < 5:
                print(f'                                {i.order_id}        | {i.size}  | {i.price}    | {i.type}  |{i.date.strftime("%d/%m/%Y | %H:%M:%S")}')
                count += 1
            else:
                break
    else:
        print("                                                 No bid orders")
    print("---------------------------------------------------------------------------------------")
    print("\t \t \t \t MARKET ORDERS ")
    print(f'Order ID | Size | Type | Date       | Time')
    if len(market_ask_orders) > 0:
        count = 0
        for i in market_ask_orders:
            if count < 5:
                print(f'{i.order_id}        | {i.size}     | {i.type}  | {i.date.strftime("%d/%m/%Y | %H:%M:%S")}')
                count += 1
            else:
                break
    else:
        print("No ask orders")
    print("---------------------------------------------------------------------------------------")
    print(f'                                Order ID | Size | Type | Date      | Time')
    if len(market_bid_orders) > 0:
        count = 0
        for i in market_bid_orders:
            if count < 5:
                print(f'                                {i.order_id}        | {i.size}     | {i.type}  |{i.date.strftime("%d/%m/%Y | %H:%M:%S")}')
                count += 1
            else:
                break
    else:
        print("                                                 No bid orders")
def send_notification(notification_for, order_id, transaction_id, price, size, order_type):
    if notification_for == "seller":
        print("Notification to Seller :")
        print(f'Your order has been {order_type} filled for {size} units at price {price} to buyer with order ID {order_id}. Your transaction ID is {transaction_id}')
    if notification_for == "buyer":
        print("Notification to Buyer :")
        print(f'Your order has been {order_type} filled for {size} units at price {price} from seller with order ID {order_id}. Your transaction ID is {transaction_id}')

def check_order_fullfillment():
    #  Check if there is any Limit Order in the book
    if len(limit_ask_orders) > 0 or len(limit_bid_orders) > 0:
        # First fullfill if any market order is being placed
        if len(market_bid_orders) > 0 and len(limit_ask_orders) > 0:
            #  if the size of market bid order is equal to the size of top limit ask order  
            if limit_ask_orders[0].size == market_bid_orders[0].size:
                # Creates an Transaction for the order
                transaction_order = Transaction(market_bid_orders[0].order_id,limit_ask_orders[0].order_id, limit_ask_orders[0].price, market_bid_orders[0].size)
                # Sends the notifications to the buyer and seller for the current transaction
                send_notification("buyer", limit_ask_orders[0].order_id, transaction_order.transaction_id, limit_ask_orders[0].price,limit_ask_orders[0].size, order_type = "completely")
                send_notification("seller", market_bid_orders[0].order_id, transaction_order.transaction_id, limit_ask_orders[0].price,limit_ask_orders[0].size, order_type = "completely")
                # Removes the orders from the order books
                limit_ask_orders.pop(0)
                market_bid_orders.pop(0)
            elif limit_ask_orders[0].size > market_bid_orders[0].size:
                transaction_order = Transaction(market_bid_orders[0].order_id,limit_ask_orders[0].order_id, limit_ask_orders[0].price, market_bid_orders[0].size)
                new_ask_size = limit_ask_orders[0].size - market_bid_orders[0].size
                send_notification("buyer", limit_ask_orders[0].order_id, transaction_order.transaction_id, limit_ask_orders[0].price, market_bid_orders[0].size, order_type = "completely")
                send_notification("seller", market_bid_orders[0].order_id, transaction_order.transaction_id, limit_ask_orders[0].price, market_bid_orders[0].size, order_type = "partially")
                market_bid_orders.pop(0)
                limit_ask_orders[0].size = new_ask_size
            elif limit_ask_orders[0].size < market_bid_orders[0].size:
                transaction_order = Transaction(market_bid_orders[0].order_id,limit_ask_orders[0].order_id, limit_ask_orders[0].price, limit_ask_orders[0].size)
                new_bid_size = market_bid_orders[0].size - limit_ask_orders[0].size
                send_notification("buyer", limit_ask_orders[0].order_id, transaction_order.transaction_id, limit_ask_orders[0].price,limit_ask_orders[0].size, order_type = "partially")
                send_notification("seller", market_bid_orders[0].order_id, transaction_order.transaction_id, limit_ask_orders[0].price,limit_ask_orders[0].size, order_type = "completely")
                limit_ask_orders.pop(0)
                market_bid_orders[0].size = new_bid_size
            check_order_fullfillment()
        elif len(market_ask_orders) > 0 and len(limit_bid_orders) > 0:
            if market_ask_orders[0].size == limit_bid_orders[0].size:
                transaction_order = Transaction(limit_bid_orders[0].order_id,market_ask_orders[0].order_id, limit_bid_orders[0].price, limit_bid_orders[0].size)
                send_notification("buyer", market_ask_orders[0].order_id, transaction_order.transaction_id, limit_bid_orders[0].price,market_ask_orders[0].size, order_type = "completely")
                send_notification("seller", limit_bid_orders[0].order_id, transaction_order.transaction_id, limit_bid_orders[0].price,market_ask_orders[0].size, order_type = "completely")
                market_ask_orders.pop(0)
                limit_bid_orders.pop(0)
            elif market_ask_orders[0].size > limit_bid_orders[0].size:
                transaction_order = Transaction(limit_bid_orders[0].order_id,market_ask_orders[0].order_id, limit_bid_orders[0].price, limit_bid_orders[0].size)
                new_ask_size = market_ask_orders[0].size - limit_bid_orders[0].size
                send_notification("buyer", market_ask_orders[0].order_id, transaction_order.transaction_id, limit_bid_orders[0].price, limit_bid_orders[0].size, order_type = "completely")
                send_notification("seller", limit_bid_orders[0].order_id, transaction_order.transaction_id, limit_bid_orders[0].price, limit_bid_orders[0].size, order_type = "partially")
                limit_bid_orders.pop(0)
                market_ask_orders[0].size = new_ask_size
            elif market_ask_orders[0].size < limit_bid_orders[0].size:
                transaction_order = Transaction(limit_bid_orders[0].order_id,market_ask_orders[0].order_id, limit_bid_orders[0].price, market_ask_orders[0].size)
                new_bid_size = limit_bid_orders[0].size - market_ask_orders[0].size
                send_notification("buyer", market_ask_orders[0].order_id, transaction_order.transaction_id, limit_bid_orders[0].price,market_ask_orders[0].size, order_type = "partially")
                send_notification("seller", limit_bid_orders[0].order_id, transaction_order.transaction_id, limit_bid_orders[0].price,market_ask_orders[0].size, order_type = "completely")
                market_ask_orders.pop(0)
                limit_bid_orders[0].size = new_bid_size
            check_order_fullfillment()
        if len(limit_ask_orders) > 0 and len(limit_bid_orders) > 0:
            if limit_ask_orders[0].price < limit_bid_orders[0].price:
                if limit_ask_orders[0].size == limit_bid_orders[0].size:
                    transaction_order = Transaction(limit_bid_orders[0].order_id,limit_ask_orders[0].order_id, limit_ask_orders[0].price, limit_bid_orders[0].size)
                    send_notification("buyer", limit_ask_orders[0].order_id, transaction_order.transaction_id, limit_ask_orders[0].price,limit_ask_orders[0].size, order_type = "completely")
                    send_notification("seller", limit_bid_orders[0].order_id, transaction_order.transaction_id, limit_ask_orders[0].price,limit_ask_orders[0].size, order_type = "completely")
                    limit_ask_orders.pop(0)
                    limit_bid_orders.pop(0)
                elif limit_ask_orders[0].size > limit_bid_orders[0].size:
                    transaction_order = Transaction(limit_bid_orders[0].order_id,limit_ask_orders[0].order_id, limit_ask_orders[0].price, limit_bid_orders[0].size)
                    new_ask_size = limit_ask_orders[0].size - limit_bid_orders[0].size
                    send_notification("buyer", limit_ask_orders[0].order_id, transaction_order.transaction_id, limit_ask_orders[0].price, limit_bid_orders[0].size, order_type = "completely")
                    send_notification("seller", limit_bid_orders[0].order_id, transaction_order.transaction_id, limit_ask_orders[0].price, limit_bid_orders[0].size, order_type = "partially")
                    limit_bid_orders.pop(0)
                    limit_ask_orders[0].size = new_ask_size
                elif limit_ask_orders[0].size < limit_bid_orders[0].size:
                    transaction_order = Transaction(limit_bid_orders[0].order_id,limit_ask_orders[0].order_id, limit_ask_orders[0].price, limit_ask_orders[0].size)
                    new_bid_size = limit_bid_orders[0].size - limit_ask_orders[0].size
                    send_notification("buyer", limit_ask_orders[0].order_id, transaction_order.transaction_id, limit_ask_orders[0].price,limit_ask_orders[0].size, order_type = "partially")
                    send_notification("seller", limit_bid_orders[0].order_id, transaction_order.transaction_id, limit_ask_orders[0].price,limit_ask_orders[0].size, order_type = "completely")
                    limit_ask_orders.pop(0)
                    limit_bid_orders[0].size = new_bid_size 
                check_order_fullfillment()

def place_market_order(size, type):
    market_order = MarketOrder(size, type)
    if type == "ask":
        market_ask_orders.append(market_order)
    if type == "bid":
        market_bid_orders.append(market_order)
    check_order_fullfillment()

# Places limit order and calls check order fullfillment function

def place_limit_order(size, price, type):
    global ask
    global bid
    limit_order = Order(size, type, price)
    ask_flag = 0
    bid_flag = 0
    if type == "ask":
        count = 0
        if len(limit_ask_orders) == 0:
            limit_ask_orders.append(limit_order)
            ask_flag = 1
        for i in limit_ask_orders:
            
            if price < i.price:
                
                limit_ask_orders.insert(count, limit_order)
                ask_flag = 1
                break
            elif price == i.price and limit_order.time < i.time:
                
                limit_ask_orders.insert(count, limit_order)
                ask_flag = 1
                break
            else:
                pass
            count += 1
        if ask_flag == 0:
            limit_ask_orders.append(limit_order)

    if type == "bid":
        count = 0
        if len(limit_bid_orders) == 0:
            limit_bid_orders.append(limit_order)
            bid_flag = 1
        for i in limit_bid_orders:
            if price > i.price:
                limit_bid_orders.insert(count, limit_order)
                bid_flag = 1
                break
            elif price == i.price and limit_order.time < i.time:
                limit_bid_orders.insert(count, limit_order)
                bid_flag = 1
                break
            else:
                pass
            count += 1
        if bid_flag == 0:
            limit_bid_orders.append(limit_order)
        show_data()
        check_order_fullfillment()

# Take the order_id as an argument and checks for the same in all the books, if found deletes the order

def cancel_order(order_id):
    found = False
    if order_id.startswith("LA"):
        if len(limit_ask_orders) > 0:
            count = 0
            for i in limit_ask_orders:
                if i.order_id == order_id:
                    limit_ask_orders.pop(count)
                    found = True
                count += 1
    elif order_id.startswith("LB"):            
        if len(limit_bid_orders) > 0:
            count = 0
            for i in limit_bid_orders:
                if i.order_id == order_id:
                    limit_bid_orders.pop(count)
                    found = True
                count += 1
    elif order_id.startswith("MA"):
        if len(market_ask_orders) > 0:
            count = 0
            for i in market_ask_orders:
                if i.order_id == order_id:
                    market_ask_orders.pop(count)
                    found = True
                count += 1
    elif order_id.startswith("MB"):
        if len(market_bid_orders) > 0:
            count = 0
            for i in market_bid_orders:
                if i.order_id == order_id:
                    market_bid_orders.pop(count)
                    found = True
                count += 1
    if found == False:
        print("Invalid Order ID")


    check_order_fullfillment()