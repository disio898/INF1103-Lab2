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
#total_units_processed = 0
stock_quantity_int = 0
global failed_entries
failed_entries = 0

def get_valid_input(stock_quantity):
    
    if stock_quantity == "quit":
        return False
    
    if stock_quantity.isdigit() and int(stock_quantity) >= 0:
        global stock_quantity_int
        stock_quantity_int = int(stock_quantity)
        if(inventory["Apple"] + stock_quantity_int <= 500):
            return True
        else:
            print("Alert! Stock exceeds 500!")
            return False
    else:
        print("An exception occured")   
        global failed_entries
        failed_entries += 1
        return "Continue"


while stop_prompt == False:

    stock_quantity = input("Enter stock quantity (type quit to quit): ")
    response = get_valid_input(stock_quantity) 
    if(response == True):
        inventory["Apple"] += stock_quantity_int
        total_delivery_charges += delivery_charges["Apple"]
        number_of_deliveries += 1
        print(f"Current inventory: {stock_quantity_int} \nDelivery and tax: ${delivery_charges["Apple"]*1.1}")
        print(f"Total deliveries: {number_of_deliveries} \nTotal delivery charges: ${total_delivery_charges}")
    elif(response == "Continue"):
        print(f"Total units processed: {stock_quantity_int}\nFailed entries: {failed_entries}")
    else:
        #To print out if the loop is stopped
        stop_prompt = True
        total_delivery_charges += delivery_charges["Apple"]
        print(f"Total units processed: {stock_quantity_int}\nFailed entries: {failed_entries}")
        print(f"Current inventory: {stock_quantity_int} \nDelivery and tax: ${delivery_charges["Apple"]*1.1}")
        print(f"Total deliveries: {number_of_deliveries} \nTotal delivery charges: {total_delivery_charges}")
    