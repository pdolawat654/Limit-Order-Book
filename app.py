import orderbook
import time

option = -1

while (option != 5):
    print("Enter your choice : \n 1. Place Market Order \n 2. Place Limit Order \n 3. Cancel Order \n 4. Show Order Book \n 5. Exit")
    option = int(input())
    if option == 1:
        size = int(input("Enter size : "))
        type = int(input("Enter type : \n 1. Ask \n 2. Bid \n"))
        if type == 1 and size > 0:
            orderbook.place_market_order(size,"ask")
        elif type == 2 and size > 0:
            orderbook.place_market_order(size,"bid")
        else:
            print("Invalid Output")
    elif option == 2:
        size = int(input("Enter size : "))
        price = int(input("Enter Price : "))
        type = int(input("Enter type : \n 1. Ask \n 2. Bid \n"))
        if type == 1 and price > 0 and size > 0:
            orderbook.place_limit_order(size,price,"ask")
        elif type == 2 and price > 0 and size > 0:
            orderbook.place_limit_order(size,price,"bid")
        else:
            print("Invalid Output")
    elif option == 3:
        order_id = input("Enter Order ID : ")
        orderbook.cancel_order(order_id)
    elif option == 4:
        orderbook.show_data()
    elif option == 5:
        break
    else:
        print("Invalid Input")
    