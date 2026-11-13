from typing import Any

from DigitalProduct import DigitalProduct
from PhysicalProduct import PhysicalProduct
from product import Product
from supplier import Supplier


class ProductFactory:
    """Builds the right Product subclass from a type identifier.

    Adding a new product type only requires registering it here;
    Product, Inventory and the persistence code stay unchanged.
    """

    _registry: dict[str, type[Product]] = {
        "physical": PhysicalProduct,
        "digital": DigitalProduct,
    }

    @classmethod
    def register(cls, type_name: str, product_class: type[Product]) -> None:
        cls._registry[type_name] = product_class

    @classmethod
    def available_types(cls) -> list[str]:
        return list(cls._registry)

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
        suppliers: dict[str, Supplier] | None = None,
    ) -> Product:
        """Rebuild a product. Pass a shared `suppliers` dict (keyed by supplier ID)
        so products with the same supplier end up referencing one Supplier object."""
        type_name = data.get("type")
        product_class = cls._registry.get(type_name)
        if product_class is None:
            raise ValueError(f"Unknown product type: {type_name!r}")

        supplier_data = data["supplier"]
        if suppliers is None:
            suppliers = {}
        supplier_id = str(supplier_data["supplier_id"])
        if supplier_id not in suppliers:
            suppliers[supplier_id] = Supplier.from_dict(supplier_data)

        return product_class.from_dict(data, suppliers[supplier_id])