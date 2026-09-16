inventory ={
  "Apple": 0
}

stop_prompt = False
while stop_prompt == False:

    stock_quantity = input("Enter stock quantity (type quit to quit): ")
    if stock_quantity == "quit":
            stop_prompt = True
            break
    inventory["Apple"] += stock_quantity_int