from typing import Any

from CanBeShipped import CanBeShipped
from product import Product
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped. Weight is in kilograms."""

    BASE_SHIPPING: float = 5.00
    RATE_PER_KG: float = 2.00

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        weight: float = 0.0,
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight: float = float(weight)

    @property
    def weight(self) -> float:
        return self.__weight

    @property
    def product_type(self) -> str:
        return "physical"

    def display_information(self) -> None:
        super().display_information()
        print(f"  Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        return f"{self.name} requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return round(self.BASE_SHIPPING + self.RATE_PER_KG * self.__weight, 2)

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any], supplier: Supplier) -> "PhysicalProduct":
        return cls(
            data["product_id"],
            data["name"],
            data["price"],
            data["stock"],
            supplier,
            data["weight"],
        )