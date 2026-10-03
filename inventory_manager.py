import ast

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
        print(inventory)

def add_product(product, price):
    id = 0
    for key, value in inventory.items():
        if value[0] > id:
            print(value[0])
    # assign numerical id greater than the highest current id in current inventory
    inventory.add(product, [id+1, 0, price])

load_inventory()


