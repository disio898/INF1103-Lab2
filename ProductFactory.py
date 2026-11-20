from typing import Any

from DigitalProduct import DigitalProduct
from PhysicalProduct import PhysicalProduct
from product import Product
from supplier import Supplier


class ProductFactory:
    """Factory pattern: the one place that decides which Product subclass to build.

    The rest of the program asks for a Product by type name and only ever sees
    the Product type. Adding a new product type means one new entry here
    (an accepted OCP trade-off for a small system).
    """

    _registry: dict[str, type[Product]] = {
        "physical": PhysicalProduct,
        "digital": DigitalProduct,
    }

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        **attributes: float,
    ) -> Product:
        """Create a product. `attributes` carries the type-specific value
        (weight=... for physical, download_size=... for digital)."""
        product_class = ProductFactory._registry.get(product_type)
        if product_class is None:
            raise ValueError(f"Unknown product type: {product_type}")
        return product_class(product_id, name, price, stock_quantity, supplier, **attributes)

    @classmethod
    def available_types(cls) -> list[str]:
        return list(cls._registry)

    @staticmethod
    def from_dict(
        data: dict[str, Any],
        suppliers: dict[str, Supplier] | None = None,
    ) -> Product:
        
        """Rebuild a saved product (JSON) through create().

        Pass a shared `suppliers` dict (keyed by supplier ID) so products with the
        same supplier end up referencing one Supplier object."""
        if suppliers is None:
            suppliers = {}
        supplier_data = data["supplier"]
        supplier_id = str(supplier_data["supplier_id"])
        if supplier_id not in suppliers:
            suppliers[supplier_id] = Supplier.from_dict(supplier_data)

        extras = {k: data[k] for k in ("weight", "download_size") if k in data}
        return ProductFactory.create(
            data.get("type"),
            data["product_id"],
            data["name"],
            data["price"],
            data["stock"],
            suppliers[supplier_id],
            **extras,
        )