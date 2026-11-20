import unittest

from DigitalProduct import DigitalProduct
from order import Order, OrderLine
from PhysicalProduct import PhysicalProduct
from product import Product
from ProductFactory import ProductFactory
from supplier import Supplier


class TestFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S1", "Acme", "a@acme.example")

    def test_creates_correct_subclasses(self):
        physical = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, self.supplier, weight=2.0)
        digital = ProductFactory.create("digital", "D1", "App", 9.9, 5, self.supplier, download_size=50.0)
        self.assertIsInstance(physical, PhysicalProduct)
        self.assertIsInstance(digital, DigitalProduct)
        self.assertIsInstance(physical, Product)

    def test_unknown_type_raises_clear_error(self):
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create("service", "S1", "Install", 30.0, 1, self.supplier)
        self.assertIn("Unknown product type: service", str(ctx.exception))

    def test_from_dict_round_trip_goes_through_factory(self):
        original = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, self.supplier, weight=2.0)
        rebuilt = ProductFactory.from_dict(original.to_dict())
        self.assertIsInstance(rebuilt, PhysicalProduct)
        self.assertEqual(rebuilt.weight, 2.0)


class TestValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S1", "Acme", "a@acme.example")

    def make(self, price=10.0, stock=1, kind="physical"):
        return ProductFactory.create(kind, "P1", "Thing", price, stock, self.supplier)

    def test_price_must_be_greater_than_zero(self):
        for bad in (0, -5):
            with self.assertRaises(ValueError):
                self.make(price=bad)

    def test_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            self.make(stock=-1)

    def test_subclasses_keep_the_same_rules(self):  # LSP
        for kind in ("physical", "digital"):
            with self.assertRaises(ValueError):
                self.make(price=0, kind=kind)
            with self.assertRaises(ValueError):
                self.make(stock=-1, kind=kind)

    def test_order_line_quantity_must_be_positive(self):
        product = self.make()
        for bad in (0, -3):
            with self.assertRaises(ValueError):
                OrderLine(product, bad)
            with self.assertRaises(ValueError):
                Order("O1").add_order_line(product, bad)


if __name__ == "__main__":
    unittest.main()
