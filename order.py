from discount import DiscountStrategy, NoDiscount
from product import Product


class OrderLine:
    """One product and quantity inside an Order.

    Only Order should create OrderLines (composition). It refers to a Product
    but does not own it (association). It protects its own quantity rule.
    """

    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Quantity must be a whole number.")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display_information(self) -> None:
        print(
            f"  {self.product.name} x{self.quantity} "
            f"@ ${self.product.price:.2f} = ${self.calculate_subtotal():.2f}"
        )


class Order:
    """Composition: an Order creates and manages its own OrderLine objects.

    Association: it *uses* a DiscountStrategy but does not own it, so one
    strategy object can be shared by many orders. No discount if/elif here.
    """

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        # The Order creates the line itself; lines are never passed in from outside.
        self.order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, product_id: str) -> bool:
        """Remove (and so destroy) the line for this product. True if one was removed."""
        for line in self.order_lines:
            if line.product.product_id == product_id:
                self.order_lines.remove(line)
                return True
        return False

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)

    def display_information(self) -> None:
        print(f"Order {self.order_id}:")
        for line in self.order_lines:
            line.display_information()
        print(f"  Total: ${self.calculate_total():.2f}")