inventory ={
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
    
    if stock_quantity.isdigit():
        stock_quantity_int = int(stock_quantity)
        inventory["Apple"] += stock_quantity_int
        print(f"Current inventory: {stock_quantity_int}")
    else:
        print("An exception occured")    
  