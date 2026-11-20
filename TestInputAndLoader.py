import contextlib
import io
import os
import tempfile
import unittest
from unittest import mock

from inputhelpers import get_positive_float
from inventory import Inventory
from ProductLoader import load_products
from supplier import Supplier

CSV = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


def run_quietly(func, *args):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


class TestGetPositiveFloat(unittest.TestCase):
    def test_asks_again_until_valid(self):
        with mock.patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            value, output = run_quietly(get_positive_float, "Price: ")
        self.assertEqual(value, 12.50)
        self.assertEqual(
            output.splitlines(),
            ["Please enter a valid number, e.g. 12.50", "Please enter a number greater than zero."],
        )

    def test_zero_rejected(self):
        with mock.patch("builtins.input", side_effect=["0", "1"]):
            value, _ = run_quietly(get_positive_float, "Price: ")
        self.assertEqual(value, 1.0)


class TestLoadProducts(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S1", "Acme", "a@acme.example")
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = os.path.join(self.tmp.name, "products.csv")
        with open(self.path, "w", newline="") as f:
            f.write(CSV)

    def test_bad_rows_skipped_and_good_rows_load(self):
        inventory = Inventory()
        _, output = run_quietly(load_products, self.path, inventory, self.supplier)
        self.assertEqual([p.product_id for p in inventory.products], ["P001", "D001", "P003"])
        lines = output.splitlines()
        self.assertIn("Unknown product type: service", lines[0])
        self.assertIn("Row 5 skipped", lines[1])
        self.assertEqual(lines[2:], ["3 products loaded.", "Load attempt finished."])

    def test_missing_file_handled(self):
        inventory = Inventory()
        _, output = run_quietly(load_products, self.path + ".missing", inventory, self.supplier)
        self.assertEqual(inventory.products, [])
        self.assertIn("Products file not found", output)
        self.assertIn("Load attempt finished.", output)
        self.assertNotIn("products loaded", output)


if __name__ == "__main__":
    unittest.main()
