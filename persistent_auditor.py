#import datetime;
import ast
 
#Saved inventory to be loaded from inventory.txt instead
#This inventory holds the current inventory in the application state
#Inventory values go here too before appending to inventory.txt file 
inventory = { 
#item name as key: [itemid, quantity]
  'Wireless Mouse': [1001, 0], 'keyboard': [1002, 0], 'USB cable': [1003, 0] #default values when inventory.txt is not filled
}

delivery_charges = {
    #prices in $, current delivery charges are fixed regardless of amount ordered
    "Apple": 0.5,
    "Wireless Mouse": 1,
    "keyboard": 1,
    "USB cable": 1
}
number_of_deliveries = 0
total_delivery_charges = 0
stop_prompt = False
#total_units_processed = 0
stock_quantity_int = 0
stock_quantity_int_current_session = 0
global failed_entries
failed_entries = 0
processed_delivery = [0,0,0]
#All orders go here before appending to the order.txt file
current_session_order = [] #<--History Tracking part that was pushed together with step 1(persistence) instead of a separate step
order_history_aggregate = {'Wireless Mouse': [1001, 0], 'keyboard': [1002, 0], 'USB cable': [1003, 0]}

#def load_history():
#    invfile = open("inventory.txt", "r")
#    global order_history
#    order_history = invfile.read()
#    invfile.close()
#    print(order_history)
#    order_history = ast.literal_eval(inventory)[1]

def load_inventory():
    invfile = open("inventory.txt", "r")
    global inventory 
    inventory = invfile.read()
    invfile.close()
    inventory = ast.literal_eval(inventory)[0]

def save_inventory():
    invfile = open("inventory.txt", "w")
    #print("current session order: ", current_session_order)
    invfile.write("["+ str(inventory) + "," + str(current_session_order)+"]")
    print("Saved to inventory.txt successfully")

def save_orderHistory():
    orderFile = open("order.txt", "a")
    print(current_session_order)
    orderFile.write(str(current_session_order))

def save_state(item_order, item_quantity):
    #get item id
    item_id = inventory[item_order][0]
    current_session_order.append([item_order, item_id, item_quantity])

def get_valid_input(stock_quantity):
    
    if stock_quantity == "quit":
        return False
    
    if stock_quantity.isdigit() and int(stock_quantity) >= 0:
        global stock_quantity_int
        global stock_quantity_int_current_session
        stock_quantity_int = int(stock_quantity)
        #Always check that inventory will not exceed 500
        #Lookup current inventory values
        if(inventory[item_order][1] + stock_quantity_int <= 500):
            stock_quantity_int_current_session += stock_quantity_int
            return True
        else:
            print("Alert! Stock exceeds 500!")
            return False
    else:
        print("An exception occured")   
        global failed_entries
        failed_entries += 1
        return "Continue"

def process_delivery(item_order, current_total, new_value):
    global total_delivery_charges
    global number_of_deliveries

    current_total += new_value # current inventory value + new delivery of items
    #get itemid
    item_id = inventory[item_order][0]
    update_order(item_order, new_value, item_id) #only insert the new value as I want to track order from this session only

    inventory[item_order] = [item_id ,current_total] #Sync inventory value to new total
    total_delivery_charges += delivery_charges[item_order]
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

def summary():
    global stop_prompt
    stop_prompt = True
    generate_other(processed_delivery)
    generate_report(stock_quantity_int_current_session, failed_entries)
    #save_inventory()

def get_valid_inventory_item(item_order):

    if item_order in inventory:
        return True
    else:
        return False

def update_order(item_order, new_value, item_id): # Added a part to get order_history of current session
    if item_order in order_history_aggregate:
        order_history_aggregate[item_order][1] += new_value
        print(f"New order added: item: {item_order}, item_id: {item_id}, order: {new_value}")

def display_status_order():
    print("Current orders\n")
    for item_name, item_info in order_history_aggregate.items():
        print(f"item: {item_name}, item_id: {item_info[0]}, order: {item_info[1]}")
    

load_inventory()
#load_history()

while stop_prompt == False:
    display_status_order()

    item_order = input("Enter item to order: ")
    if item_order == "quit":
        save_orderHistory()
        save_inventory()
        summary()
        break
    
    item_validity_inventory = get_valid_inventory_item(item_order)
    if(item_validity_inventory == False):
        print("Item not valid to add to inventory")
        continue

    stock_quantity = input("Enter stock quantity (type quit to quit): ")
    response = get_valid_input(stock_quantity) 
    if(response == True):
        processed_delivery = process_delivery(item_order, inventory[item_order][1], stock_quantity_int)
        generate_other(processed_delivery)
        save_state(item_order, stock_quantity)
        
    elif(response == "Continue"):
        generate_report(stock_quantity_int_current_session, failed_entries)
    else:
        #To print out if the loop is stopped
        summary()
        #stop_prompt = True
        #generate_other(processed_delivery)
        #generate_report(stock_quantity_int, failed_entries)
        save_inventory()
    