from product import Product
 
class DigitalProduct(Product):
 
    def __init__(self, product_id, name, price, stock=0, download_size=0.0):
        super().__init__(product_id, name, price, stock)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size = float(download_size)
 
    @property
    def download_size(self):
        return self.__download_size
 
    @property
    def product_type(self):
        return "digital"
 
    def display_information(self):
        super().display_information()
        print(f"  Download size: {self.__download_size:.2f} MB")
 
 
    def to_dict(self):
        data = super().to_dict()
        data["download_size"] = self.__download_size
        return data
 
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["product_id"],
            data["name"],
            data["price"],
            data["stock"],
            data["download_size"],
        )
 