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
            print(f"Total units processed: {total_units_processed }\nFailed entries: {failed_entries}")
            break
    
    if stock_quantity.isdigit() and int(stock_quantity) >= 0:
        stock_quantity_int = int(stock_quantity)
        if(inventory["Apple"] + stock_quantity_int <= 500):
            inventory["Apple"] += stock_quantity_int
            print(f"Current inventory: {stock_quantity_int}")
        else:
            print("Alert! Stock exceeds 500!")
            break
    else:
        print("An exception occured")    
        failed_entries += 1
    