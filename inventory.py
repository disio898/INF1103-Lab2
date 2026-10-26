from product import Product

class Inventory:
    def __init__(self):
        self.__products = {}

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added.")

        if product.name in self.__products:
            raise ValueError("Product already exists.")

        if any(
            p.product_id == product.product_id
            for p in self.__products.values()
        ):
            raise ValueError("Product ID already exists.")

        self.__products[product.name] = product

    def search_product(self, name):
        return self.__products.get(name)

    def get_all_products(self):
        return list(self.__products.values())

    def display_all(self):
        print("\nCurrent inventory:")
        for product in self.__products.values():
            product.display_information()

    def to_list(self):
        return [
            product.to_dict()
            for product in self.__products.values()
        ]

    def load_products(self, products):
        for product in products:
            self.add_product(product)