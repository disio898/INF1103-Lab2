from typing import Any

from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A product delivered by download. Download size is in megabytes."""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        download_size: float = 0.0,
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size: float = float(download_size)

    @property
    def download_size(self) -> float:
        return self.__download_size

    @property
    def product_type(self) -> str:
        return "digital"

    def display_information(self) -> None:
        super().display_information()
        print(f"  Download size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self) -> str:
        return f"{self.name} is delivered digitally via download."

    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any], supplier: Supplier) -> "DigitalProduct":
        return cls(
            data["product_id"],
            data["name"],
            data["price"],
            data["stock"],
            supplier,
            data["download_size"],
        )