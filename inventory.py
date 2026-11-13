from typing import Any

from product import Product


class Inventory:
    """Aggregation: groups existing Product objects but does not own their lifecycle."""

    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added.")

        if any(p.product_id == product.product_id for p in self.products):
            raise ValueError("Product ID already exists.")

        if any(p.name == product.name for p in self.products):
            raise ValueError("Product already exists.")

        self.products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the reference only. The Product itself is returned, not destroyed."""
        product = self.find_product(product_id)
        if product is not None:
            self.products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def search_product(self, term: str) -> Product | None:
        """Find a product by ID or exact name."""
        product = self.find_product(term)
        if product is not None:
            return product
        for product in self.products:
            if product.name == term:
                return product
        return None

    def get_all_products(self) -> list[Product]:
        return list(self.products)

    def display_all_products(self) -> None:
        print("\nCurrent inventory:")
        for product in self.products:
            product.display_information()

    def to_list(self) -> list[dict[str, Any]]:
        return [product.to_dict() for product in self.products]

    def load_products(self, products: list[Product]) -> None:
        for product in products:
            self.add_product(product)