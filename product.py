class Product:
    MAX_STOCK = 500

    def __init__(self, product_id, name, price, stock=0):
        if not isinstance(stock, int) or isinstance(stock, bool):
            raise ValueError("Stock must be an integer.")

        if stock < 0 or stock > self.MAX_STOCK:
            raise ValueError("Stock must be between 0 and 500.")

        if price < 0:
            raise ValueError("Price cannot be negative.")

        self.__product_id = str(product_id)
        self.__name = name
        self.__price = float(price)
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

    def update_stock(self, quantity):
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Quantity must be an integer.")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        if self.__stock + quantity > self.MAX_STOCK:
            raise ValueError("Alert! Stock exceeds 500!")

        self.__stock += quantity

    def display_information(self):
        print(
            f"Item: {self.__name}, "
            f"Item ID: {self.__product_id}, "
            f"Quantity: {self.__stock}, "
            f"Price: ${self.__price:.2f}"
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