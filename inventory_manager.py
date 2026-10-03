import ast

stop_prompt = False
inventory = {}
price_table = {
    'Wireless Mouse' : 5,
    'keyboard': 100,
    'USB cable': 3
}

def load_inventory(): #part 4 modularity
    invfile = open("inventory.json", "r")
    if open("inventory.json", "r").read() != "":
        global inventory 
        inventory = invfile.read()
        invfile.close()
        inventory = ast.literal_eval(inventory)[0]
        #print(inventory)

def add_product(product, price):
    id = 0
    for key, value in inventory.items():
        if value[0] > id:
            id = value[0]
    # assign numerical id greater than the highest current id in current inventory
    id+=1
    inventory.update({product: [id, 0, f"${price}"]})
    price_table.update({product: f"${price}"})

def update_stock(product):
    if product in inventory:
        new_stock = input("Enter new stock value")
        inventory[product][2] = new_stock
    else:
        print("Product not found")

def search_product(product_search):
    if product_search in inventory:
        return print(f"item: {product_search}, id: {inventory[product_search][0]}, stock: {inventory[product_search][1]}, price: {inventory[product_search][2]}")
    else:
        for key, value in inventory.items():
            # search by id
            if(str(value[0]) == product_search):
                return print(key, f"id: {value[0]}, stock: {value[1]}, price: {value[2]}")
        return print("Item not found")

def save_inventory():
    return
    
load_inventory()

def format_inventory_display():
    for key, value in inventory.items():
        print(key, f"id: {value[0]}, stock: {value[1]}, price: {value[2]}")

while stop_prompt == False:
    print("Menu")
    user_input = input("1.Display All Products\n2.Add Product\n3.Update Stock\n4.Search Product\n5.Save Inventory\n6.Exit\nEnter(1-6):")
    print(user_input)
    if(user_input=="1"):
        format_inventory_display()
        continue
    elif(user_input=="2"):
        product = input("Enter product: ")
        price = input("Enter price: ")
        add_product(product, price)
        continue 
    elif(user_input=="3"):
        product = input("Enter product: ")
        update_stock(product)
    elif(user_input=="4"):
        search = input("Search product: ")
        search_product(search)
    elif(user_input=="5"):
        save_inventory()