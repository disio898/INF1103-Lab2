import csv

from inventory import Inventory
from ProductFactory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Load products from a CSV file into the inventory.

    Columns: product_type, product_id, name, price, stock_quantity.
    A missing file is reported; a bad row is reported and skipped.
    """
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip header row
            for row_number, row in enumerate(reader, start=2):
                try:
                    if len(row) != 5:
                        raise ValueError("expected 5 columns")
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(
                        product_type.strip(),
                        product_id.strip(),
                        name.strip(),
                        float(price),
                        int(stock),
                        supplier,
                    )
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as error:
                    print(f"Row {row_number} skipped: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")