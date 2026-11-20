import ast
import inspect
import textwrap
import unittest

import order as order_module
from discount import (
    BulkDiscount,
    DiscountStrategy,
    NoDiscount,
    PercentageDiscount,
    StudentDiscount,
)
from order import Order
from ProductFactory import ProductFactory
from supplier import Supplier


class TestDiscounts(unittest.TestCase):
    def setUp(self) -> None:
        supplier = Supplier("S1", "Acme", "a@acme.example")
        self.product = ProductFactory.create("physical", "P1", "Thing", 50.0, 10, supplier, weight=1.0)

    def order_of_250(self, discount=None) -> Order:
        order = Order("O1", discount)
        order.add_order_line(self.product, 5)  # 5 x 50 = 250
        return order

    def test_default_is_no_discount(self):
        self.assertIsInstance(Order("O1").discount, NoDiscount)
        self.assertEqual(self.order_of_250().calculate_total(), 250)

    def test_bulk_then_percentage_via_set_discount(self):
        order = self.order_of_250(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225)

    def test_bulk_below_threshold_unchanged(self):
        self.assertEqual(BulkDiscount(200, 20).apply(199.99), 199.99)

    def test_new_strategy_needs_no_order_change(self):
        class HalfPrice(DiscountStrategy):  # defined outside Order, Order untouched
            def apply(self, total: float) -> float:
                return total / 2

        self.assertEqual(self.order_of_250(HalfPrice()).calculate_total(), 125)

    def test_student_discount_is_five_percent(self):
        self.assertAlmostEqual(self.order_of_250(StudentDiscount()).calculate_total(), 237.5)

    def test_strategy_is_abstract(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_invalid_percentage_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(150)

    def test_order_has_no_discount_if_elif_logic(self):
        tree = ast.parse(textwrap.dedent(inspect.getsource(order_module.Order.calculate_total)))
        self.assertFalse([n for n in ast.walk(tree) if isinstance(n, ast.If)])
        names = {n.id for n in ast.walk(ast.parse(inspect.getsource(order_module))) if isinstance(n, ast.Name)}
        self.assertFalse(names & {"PercentageDiscount", "BulkDiscount", "StudentDiscount"})

    def test_strategy_can_be_shared_between_orders(self):
        shared = PercentageDiscount(10)
        a, b = self.order_of_250(shared), self.order_of_250(shared)
        self.assertIs(a.discount, b.discount)


if __name__ == "__main__":
    unittest.main()
