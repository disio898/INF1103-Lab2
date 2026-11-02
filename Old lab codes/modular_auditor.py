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
processed_delivery = [0,0,0]

def get_valid_input(stock_quantity):
    
    if stock_quantity == "quit":
        return False
    
    if stock_quantity.isdigit() and int(stock_quantity) >= 0:
        global stock_quantity_int
        stock_quantity_int = int(stock_quantity)
        print(f"testing: {inventory['Apple']}")
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

def process_delivery(current_total, new_value):
    global total_delivery_charges
    global number_of_deliveries
    current_total += new_value # current inventory value + new delivery of items
    inventory["Apple"] = current_total #Sync inventory value to new total
    total_delivery_charges += delivery_charges["Apple"]
    number_of_deliveries += 1
    return [current_total, total_delivery_charges, number_of_deliveries]

def calculate_tax(amount):
    return amount*1.1

def generate_report(total_units, failed_attempts):
    print(f"Report:\nTotal units processed: {total_units}\nFailed entries: {failed_attempts}")
    return

def generate_other(processed_delivery):
    print(f"Current inventory: {processed_delivery[0]} \nDelivery and tax: ${calculate_tax(processed_delivery[1])}")
    print(f"Total deliveries: {processed_delivery[2]}")

while stop_prompt == False:
    stock_quantity = input("Enter stock quantity (type quit to quit): ")
    response = get_valid_input(stock_quantity) 
    if(response == True):
        processed_delivery = process_delivery(inventory["Apple"], stock_quantity_int)
        generate_other(processed_delivery)
    elif(response == "Continue"):
        generate_report(stock_quantity_int, failed_entries)
    else:
        #To print out if the loop is stopped
        stop_prompt = True
        generate_other(processed_delivery)
        generate_report(stock_quantity_int, failed_entries)
    