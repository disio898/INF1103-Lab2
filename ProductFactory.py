from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
 
 
class ProductFactory:
    """Builds the right Product subclass from a type identifier.
 
    Adding a new product type only requires registering it here;
    Product, Inventory and the persistence code stay unchanged.
    """
 
    _registry = {
        "physical": PhysicalProduct,
        "digital": DigitalProduct,
    }
 
    @classmethod
    def register(cls, type_name, product_class):
        cls._registry[type_name] = product_class
 
    @classmethod
    def available_types(cls):
        return list(cls._registry)
 
    @classmethod
    def from_dict(cls, data):
        type_name = data.get("type")
        product_class = cls._registry.get(type_name)
        if product_class is None:
            raise ValueError(f"Unknown product type: {type_name!r}")
        return product_class.from_dict(data)