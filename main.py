import json
from pathlib import Path

from inventory import Inventory
from order import Order
from supplier import Supplier
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from ProductFactory import ProductFactory
from CanBeShipped import CanBeShipped

DATA_FILE = Path(__file__).with_name("inventory.json")

failed_entries = 0
order_history = []  # [product name, quantity] for this session
suppliers = {}  # supplier_id -> Supplier, shared so products reuse one object
orders = []  # Orders created this session


def load_inventory(inventory):
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        products = [ProductFactory.from_dict(item, suppliers) for item in data]
        inventory.load_products(products)
        print("Inventory loaded successfully.")
    except (OSError, json.JSONDecodeError, KeyError, ValueError, TypeError) as error:
        print(f"Unable to load inventory: {error}")


def save_inventory(inventory):
    global failed_entries
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(inventory.to_list(), file, indent=4)
        print("Inventory saved successfully.")
    except OSError as error:
        print(f"Unable to save inventory: {error}")
        failed_entries += 1


def add_sample_products(inventory):
    tech = Supplier("S001", "TechSource Ltd", "sales@techsource.example")
    soft = Supplier("S002", "SoftWorks", "hello@softworks.example")
    suppliers.update({tech.supplier_id: tech, soft.supplier_id: soft})
    inventory.load_products([
        PhysicalProduct("P001", "Wireless Mouse", 25.00, 0, tech, 0.1),
        PhysicalProduct("P002", "Keyboard", 45.00, 0, tech, 0.8),
        DigitalProduct("D001", "Photo Editor", 30.00, 0, soft, 250.0),
    ])


def get_or_create_supplier():
    """Reuse an existing supplier by ID, or create a new one."""
    supplier_id = input("Enter supplier ID: ").strip()
    if not supplier_id:
        raise ValueError("Supplier ID cannot be empty.")
    if supplier_id in suppliers:
        print("Using existing supplier:")
        suppliers[supplier_id].display_information()
        return suppliers[supplier_id]
    name = input("Enter supplier name: ").strip()
    email = input("Enter supplier contact email: ").strip()
    if not name or not email:
        raise ValueError("Supplier name and email cannot be empty.")
    suppliers[supplier_id] = Supplier(supplier_id, name, email)
    return suppliers[supplier_id]


def add_product_menu(inventory):
    global failed_entries
    try:
        kind = input("Product type (physical/digital): ").strip().lower()
        if kind not in ("physical", "digital"):
            print("Product type must be 'physical' or 'digital'.")
            failed_entries += 1
            return

        product_id = input("Enter product ID: ").strip()
        name = input("Enter product name: ").strip()
        if not product_id or not name:
            print("Product ID and name cannot be empty.")
            failed_entries += 1
            return

        price = float(input("Enter product price: $"))
        stock = int(input("Enter initial stock (0-500): "))
        supplier = get_or_create_supplier()

        if kind == "physical":
            weight = float(input("Enter weight (kg): "))
            product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
        else:
            size = float(input("Enter download size (MB): "))
            product = DigitalProduct(product_id, name, price, stock, supplier, size)

        inventory.add_product(product)
        print("Product added successfully.")

    except (ValueError, TypeError) as error:
        print(f"Invalid input: {error}")
        failed_entries += 1


def update_stock_menu(inventory):
    global failed_entries
    term = input("Enter product ID or name: ").strip()
    product = inventory.search_product(term)

    if product is None:
        print("Product not found.")
        return

    product.display_information()
    try:
        quantity = int(input("Enter quantity to add (negative to remove stock): "))
        product.update_stock(quantity)
        print("Stock updated successfully.")
        product.display_information()
        order_history.append([product.name, quantity])
    except ValueError as error:
        print(f"Unable to update stock: {error}")
        failed_entries += 1


def search_product_menu(inventory):
    term = input("Enter product ID or name: ").strip()
    product = inventory.search_product(term)

    if product is None:
        print("Product not found.")
        return

    product.display_information()
    product.supplier.display_information()
    print(f"  {product.get_fulfilment_info()}")
    if isinstance(product, CanBeShipped):
        print(f"  Shipping cost: ${product.calculate_shipping_cost():.2f}")


def create_order_menu(inventory):
    global failed_entries
    order_id = input("Enter order ID: ").strip()
    if not order_id:
        print("Order ID cannot be empty.")
        failed_entries += 1
        return

    order = Order(order_id)
    print("Add products to the order (blank product to finish).")
    while True:
        term = input("Product ID or name: ").strip()
        if not term:
            break
        product = inventory.search_product(term)
        if product is None:
            print("Product not found.")
            continue
        try:
            quantity = int(input("Quantity: "))
            order.add_order_line(product, quantity)
        except ValueError as error:
            print(f"Invalid quantity: {error}")
            failed_entries += 1

    if order.order_lines:
        orders.append(order)
        order.display_information()
    else:
        print("Order has no lines and was not created.")


def display_status_order():
    print("\nSession orders:")
    for item in order_history:
        print(item)


def summary(inventory):
    total_units = sum(abs(quantity) for _, quantity in order_history)
    inventory.display_all_products()
    print(f"\nReport:\nTotal deliveries this session: {len(order_history)}")
    print(f"Total units processed: {total_units}")
    print(f"Orders created: {len(orders)}\nFailed entries: {failed_entries}")


def main():
    inventory = Inventory()
    if DATA_FILE.exists():
        load_inventory(inventory)
    else:
        print("No saved inventory found. Starting with sample products.")
        add_sample_products(inventory)

    while True:
        display_status_order()
        choice = input(
            "Enter (1-6) or quit: \n"
            "1: display inventory \n2: add product \n"
            "3: update stock(order/remove) \n4: search product \n"
            "5: save inventory \n6: create order\n"
        ).strip().lower()

        if choice == "quit":
            save_inventory(inventory)
            summary(inventory)
            break
        elif choice == "1":
            inventory.display_all_products()
        elif choice == "2":
            add_product_menu(inventory)
        elif choice == "3":
            update_stock_menu(inventory)
        elif choice == "4":
            search_product_menu(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            create_order_menu(inventory)
        else:
            global failed_entries
            print("Invalid option.")
            failed_entries += 1


if __name__ == "__main__":
    main()