inventory = {
  "Apple": 0 
}

stop_prompt = False
total_units_processed = 0
failed_entries = 0

while stop_prompt == False:

    stock_quantity = input("Enter stock quantity (type quit to quit): ")
    if stock_quantity == "quit":
            stop_prompt = True
            break
    
    if stock_quantity.isdigit() and int(stock_quantity) >= 0:
        stock_quantity_int = int(stock_quantity)
        #For Step 6, "Manage State: Keep a running total of the inventory" is already fulfilled
        inventory["Apple"] += stock_quantity_int 
        print(f"Current inventory: {stock_quantity_int}")
    else:
        print("An exception occured")    
  