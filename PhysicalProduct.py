from product import Product
 
 
class PhysicalProduct(Product):
 
    BASE_SHIPPING = 5.00
    RATE_PER_KG = 2.00
 
    def __init__(self, product_id, name, price, stock=0, weight=0.0):
        super().__init__(product_id, name, price, stock)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight = float(weight)
 
    @property
    def weight(self):
        return self.__weight
 
    @property
    def product_type(self):
        return "physical"
 
    def display_information(self):
        super().display_information()
        print(f"  Weight: {self.__weight:.2f} kg")
 
 
    def to_dict(self):
        data = super().to_dict()
        data["weight"] = self.__weight
        return data
 
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["product_id"],
            data["name"],
            data["price"],
            data["stock"],
            data["weight"],
        )