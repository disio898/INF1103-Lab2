from abc import ABC, abstractmethod
from typing import Any

from supplier import Supplier


class Product(ABC):
    """Abstract base class for every product in the inventory."""

    MAX_STOCK: int = 500
    TAX_RATE: float = 0.1

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
    ) -> None:
        if not isinstance(stock, int) or isinstance(stock, bool):
            raise ValueError("Stock must be an integer.")

        if stock < 0 or stock > self.MAX_STOCK:
            raise ValueError("Stock must be between 0 and 500.")

        if price <= 0:
            raise ValueError("Price must be greater than zero.")

        self.__product_id: str = str(product_id)
        self.__name: str = name
        self.__price: float = float(price)
        self.__stock: int = stock
        self.__price_w_tax: float = round(self.__price * (1 + self.TAX_RATE), 2)
        # Association: the Supplier is created independently and only referenced.
        self.__supplier: Supplier = supplier

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def price_w_tax(self) -> float:
        return self.__price_w_tax

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> None:
        """Add stock (positive) or remove stock (negative)."""
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Quantity must be an integer.")

        if self.__stock + quantity > self.MAX_STOCK:
            raise ValueError("Alert! Stock exceeds 500!")

        if self.__stock + quantity < 0:
            raise ValueError("Cannot remove more stock than is available.")

        self.__stock += quantity

    def display_information(self) -> None:
        print(
            f"Item: {self.__name}, "
            f"Item ID: {self.__product_id}, "
            f"Quantity: {self.__stock}, "
            f"Price: ${self.__price:.2f}, "
            f"Price W Tax: ${self.__price_w_tax:.2f}, "
            f"Supplier: {self.__supplier.name}"
        )

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return a message describing how this product is fulfilled."""

    @property
    @abstractmethod
    def product_type(self) -> str:
        """Type identifier used for persistence (e.g. 'physical')."""

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.product_type,
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "price_w_tax": self.__price_w_tax,
            "supplier": self.__supplier.to_dict(),
        }