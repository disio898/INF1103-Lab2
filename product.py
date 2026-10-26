class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if not isinstance(stock, int) or isinstance(stock, bool) or not 0 <= stock <= 500:
            raise ValueError("Stock must be an integer between 0 and 500.")

        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    def update_stock(self, quantity: int):
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Quantity must be an integer.")

        new_stock = self.__stock + quantity

        if new_stock < 0:
            raise ValueError("Stock cannot be negative.")
        if new_stock > 500:
            raise ValueError("Stock cannot exceed 500.")

        self.__stock = new_stock

    def display_information(self):
        print(
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )

    def to_dict(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["product_id"],
            data["name"],
            data["price"],
            data["stock"]
        )