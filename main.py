#import datetime;
import json
import ast
from product import Product
from inventory import Inventory
from pathlib import Path
DATA_FILE = Path(__file__).with_name("inventory.json")
price_table = {
    'Wireless Mouse' : 5,
    'keyboard': 100,
    'USB cable': 3
}
#Saved inventory to be loaded from inventory.txt instead
#This inventory holds the current inventory in the application state
#Inventory values go here too before appending to inventory.txt file 
#inventory = { 
#item name as key: [itemid, quantity]
#  'Wireless Mouse': [1001, 0, f"${price_table["Wireless Mouse"]}"], 'keyboard': [1002, 0, f"${price_table["keyboard"]}"], 'USB cable': [1003, 0, f"${price_table["USB cable"]}"] #default values when inventory.txt is not filled
#}


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
order_history = []
loaded_products = []
inventory = Inventory()

def load_inventory(): #part 4 modularity
    #invfile = open("inventory.json", "r")
    
    global inventory 
    #inventory = invfile.read()
    #invfile.close()
    print(inventory)
    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)
    print(data)
    global loaded_products 
    loaded_products = [
        Product.from_dict(item)
        for item in data
    ]
    
    temporary_inventory = Inventory()
    for product in loaded_products:
        temporary_inventory.add_product(product)
    for product in temporary_inventory.get_all_products():
        inventory.add_product(product)
    print("Inventory loaded successfully.")

def load_history(): #part 4 modularity
    invfile = open("inventory.json", "r")
    if open("inventory.json", "r").read() != "":
        global order_history
        order_history = invfile.read()
        invfile.close()
        order_history = ast.literal_eval(order_history)[1]
        print("order hist: ", order_history)
    else:
        order_history = ""

#def save_inventory(): #part 4 modularity
#    
#    with open("inventory.json", "r") as f:
#        if(str(f.read()) == ""):
#            f.close()
#            invfile = open("inventory.json", "w")
#            invfile.write("["+ str(inventory) +",[[" + str(order_history) + str(current_session_order)+ "," + str(order_history_aggregate) +"]]]")
#        else:
#            f.close()
#            invfile = open("inventory.txt", "w")
#            order_history.append([current_session_order, order_history_aggregate])
#            print("Current sess order: ", current_session_order)
#            print("aggregate: " , order_history_aggregate)
#            print("order history:", order_history)
#            #print("to save order history: ", order_history)
#            #print("current session order: ", current_session_order)
#            # save total inventory, sequence of orders and total order based on item per session
#            #print(str(order_history))
#            invfile.write("["+ str(inventory) + "," + str(order_history) + "]" )
#    print("Saved to inventory.json successfully")
#

def save_inventory(inventory):
    data = [
        product.to_dict()
        for product in inventory.get_all_products()
    ]

    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Inventory saved successfully.")

    except OSError as error:
        print(f"Unable to save inventory: {error}")
        failed_entries += 1

def save_orderHistory():
    orderFile = open("order.txt", "a")
    orderFile.write("[" + str(current_session_order)+ "," + str(order_history_aggregate) +"]")

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

    inventory[item_order] = [item_id ,current_total, f"${price_table[item_order]}"] #Sync inventory value to new total
    total_delivery_charges += delivery_charges[item_order]
    number_of_deliveries += 1
    return [current_total, total_delivery_charges, number_of_deliveries]

def calculate_tax(amount):
    return amount*1.1

def generate_report(failed_attempts):
    total_units = 0
    for items in order_history:
        total_units+=items[1]
    print(f"Report:\nTotal units processed: {total_units}\nFailed entries: {failed_attempts}")
    return

#def generate_other(processed_delivery, item_name):
#    print(f"Current inventory of {item_name}: {processed_delivery[0]} \nDelivery and tax: ${calculate_tax(processed_delivery[1])}")
#    print(f"Current inventory of all goods: {inventory}")
#    print(f"Total deliveries in this session: {processed_delivery[2]}")

def generate_other_summary():
    print(f"Current inventory of all goods: {inventory.display_all}")
    print(f"Total deliveries in this session: {len(order_history)}")

def summary():
    global stop_prompt
    stop_prompt = True
    generate_other_summary()
    generate_report(failed_entries)
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
    print("Current orders")
    for item in order_history:
	    print(item)
    #for item_name, item_info in order_history_aggregate.items():
    #    print(f"item: {item_name}, item_id: {item_info[0]}, order: {item_info[1]}")
    
# adding some items as default values
def add_sample_products(inventory):
    sample_products = [
        Product("P001", "Wireless Mouse", 25.00, 0),
        Product("P002", "Keyboard", 45.00, 0),
        Product("P003", "USB Cable", 8.00, 0)
    ]

    for product in sample_products:
        inventory.add_product(product)


if not DATA_FILE.exists():
    print("No saved inventory found. Starting with sample products.")
    add_sample_products(inventory)
else:
    load_inventory()
#load_history()

def add_product_menu(inventory):
    global failed_entries
    try:
        product_id = input("Enter product ID: ").strip()
        name = input("Enter product name: ").strip()

        if not product_id or not name:
            print("Product ID and name cannot be empty.")
            failed_entries += 1
            return

        price = float(input("Enter product price: $"))
        stock = int(input("Enter initial stock (0-500): "))

        product = Product(product_id, name, price, stock)
        inventory.add_product(product)

        print("Product added successfully.")

    except ValueError as error:
        print(f"Invalid input: {error}")
        failed_entries += 1
    except TypeError as error:
        print(f"Unable to add product: {error}")
        failed_entries += 1


def update_stock_menu(inventory):
    search_term = input("Enter product ID or name: ").strip()
    product = inventory.search_product(search_term)

    if product is None:
        print("Product not found.")
        return

    product.display_information()

    try:
        quantity = int(
            input("Enter quantity to add (negative to remove stock): ")
        )
        product.update_stock(quantity)
        print("Stock updated successfully.")
        product.display_information()
        order_processed(product.name, quantity)
    except ValueError as error:
        print(f"Unable to update stock: {error}")
        failed_entries += 1

def order_processed(product, quantity):
    order_history.append([product, quantity])
    print(order_history)

def search_product_menu(inventory):
    search_term = input("Enter product ID or name: ").strip()
    product = inventory.search_product(search_term)

    if product is None:
        print("Product not found.")
    else:
        product.display_information()



while stop_prompt == False:
    
    display_status_order()

    item_order = input("Enter (1-5) or quit: \n1: display inventory \n2: add product \n3: update stock(order/remove) \n4: search product \n5: save inventory\n")
    if item_order == "quit":
        #save_orderHistory()
        save_inventory(inventory)
        summary()
        break
    elif item_order == "1":
        inventory.display_all()
        continue
    elif item_order == "2":
        add_product_menu(inventory)
        continue
    elif item_order == "3":
        update_stock_menu(inventory)
        continue
    elif item_order == "4":
        search_product_menu(inventory)
        continue
    elif item_order == "5":
        save_inventory(inventory)
    
    #item_validity_inventory = get_valid_inventory_item(item_order)
    #if(item_validity_inventory == False):
    #    print("Item not valid to add to inventory")
    #    continue

    #stock_quantity = input("Enter stock quantity (type quit to quit): ")
    #response = get_valid_input(stock_quantity) 
    #if(response == True):
    #    processed_delivery = process_delivery(item_order, inventory[item_order][1], stock_quantity_int)
    #    generate_other(processed_delivery, item_order)
    #    save_state(item_order, stock_quantity)
        
    elif(item_order == "Continue"):
        generate_report(failed_entries)
    else:
        #To print out if the loop is stopped
        summary()
        save_inventory(inventory)
    