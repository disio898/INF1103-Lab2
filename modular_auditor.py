inventory ={
  "Apple": 0
}

delivery_charges = {
    #prices in $, current delivery charges are fixed regardless of amount ordered
    "Apple": 0.5
}
number_of_deliveries = 0
total_delivery_charges = 0
stop_prompt = False
total_units_processed = 0
failed_entries = 0

while stop_prompt == False:

    stock_quantity = input("Enter stock quantity (type quit to quit): ")
    if stock_quantity == "quit":
            stop_prompt = True
            total_delivery_charges += delivery_charges["Apple"]
            print(f"Total units processed: {total_units_processed }\nFailed entries: {failed_entries}")
            print(f"Current inventory: {stock_quantity_int} \n Delivery and tax {delivery_charges["Apple"]*1.1}")
            print(f"Total deliveries: {number_of_deliveries} \n Total delivery charges: {total_delivery_charges}")
            break
    
    if stock_quantity.isdigit() and int(stock_quantity) >= 0:
        stock_quantity_int = int(stock_quantity)
        if(inventory["Apple"] + stock_quantity_int <= 500):
            inventory["Apple"] += stock_quantity_int
            total_delivery_charges += delivery_charges["Apple"]
            number_of_deliveries += 1
            print(f"Current inventory: {stock_quantity_int} \n Delivery and tax {delivery_charges["Apple"]*1.1}")
            print(f"Total deliveries: {number_of_deliveries} \n Total delivery charges: {total_delivery_charges}")
        else:
            print("Alert! Stock exceeds 500!")
            break
    else:
        print("An exception occured")    
        failed_entries += 1
    