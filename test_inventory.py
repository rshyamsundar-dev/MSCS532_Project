"""
test_inventory.py

Unit tests for the Dynamic Inventory Management proof of concept.
"""

import unittest

from inventory_manager import InventoryManager
from product import Product


class TestProduct(unittest.TestCase):
    """Tests for the Product class."""

    def test_create_valid_product(self):
        product = Product(
            "P101",
            "Keyboard",
            "Electronics",
            50.00,
            12
        )

        self.assertEqual(product.product_id, "P101")
        self.assertEqual(product.name, "Keyboard")
        self.assertEqual(product.category, "Electronics")
        self.assertEqual(product.price, 50.00)
        self.assertEqual(product.quantity, 12)

    def test_empty_product_id_raises_error(self):
        with self.assertRaises(ValueError):
            Product(
                "",
                "Keyboard",
                "Electronics",
                50.00,
                12
            )

    def test_negative_price_raises_error(self):
        with self.assertRaises(ValueError):
            Product(
                "P101",
                "Keyboard",
                "Electronics",
                -50.00,
                12
            )

    def test_negative_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            Product(
                "P101",
                "Keyboard",
                "Electronics",
                50.00,
                -1
            )

    def test_update_quantity(self):
        product = Product(
            "P101",
            "Keyboard",
            "Electronics",
            50.00,
            12
        )

        product.update_quantity(25)

        self.assertEqual(product.quantity, 25)


class TestInventoryManager(unittest.TestCase):
    """Tests for the InventoryManager class."""

    def setUp(self):
        self.inventory = InventoryManager()

        self.keyboard = Product(
            "P101",
            "Keyboard",
            "Electronics",
            50.00,
            12
        )

        self.mouse = Product(
            "P102",
            "Mouse",
            "Electronics",
            20.00,
            30
        )

        self.monitor = Product(
            "P103",
            "Monitor",
            "Electronics",
            200.00,
            8
        )

        self.chair = Product(
            "P104",
            "Office Chair",
            "Furniture",
            150.00,
            5
        )

        for product in [
            self.keyboard,
            self.mouse,
            self.monitor,
            self.chair
        ]:
            self.inventory.add_product(product)

    def test_add_product(self):
        product = Product(
            "P105",
            "Notebook",
            "Office Supplies",
            6.50,
            40
        )

        self.inventory.add_product(product)

        self.assertEqual(
            self.inventory.find_product("P105"),
            product
        )

    def test_add_duplicate_product_raises_error(self):
        duplicate = Product(
            "P101",
            "Duplicate Keyboard",
            "Electronics",
            60.00,
            10
        )

        with self.assertRaises(ValueError):
            self.inventory.add_product(duplicate)

    def test_find_existing_product(self):
        result = self.inventory.find_product("P103")

        self.assertEqual(result, self.monitor)

    def test_find_missing_product_returns_none(self):
        result = self.inventory.find_product("P999")

        self.assertIsNone(result)

    def test_update_quantity(self):
        self.inventory.update_quantity("P102", 3)

        self.assertEqual(
            self.inventory.find_product("P102").quantity,
            3
        )

    def test_update_missing_product_raises_error(self):
        with self.assertRaises(KeyError):
            self.inventory.update_quantity("P999", 10)

    def test_update_negative_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            self.inventory.update_quantity("P103", -5)

    def test_get_products_by_category(self):
        products = self.inventory.get_products_by_category(
            "Electronics"
        )

        product_ids = {
            product.product_id
            for product in products
        }

        self.assertEqual(
            product_ids,
            {"P101", "P102", "P103"}
        )

    def test_missing_category_returns_empty_list(self):
        products = self.inventory.get_products_by_category(
            "Clothing"
        )

        self.assertEqual(products, [])

    def test_products_sorted_by_price(self):
        products = self.inventory.get_products_sorted_by_price()

        prices = [
            product.price
            for product in products
        ]

        self.assertEqual(
            prices,
            [20.00, 50.00, 150.00, 200.00]
        )

    def test_get_lowest_stock_product(self):
        product = self.inventory.get_lowest_stock_product()

        self.assertEqual(product.product_id, "P104")
        self.assertEqual(product.quantity, 5)

    def test_lowest_stock_after_quantity_update(self):
        self.inventory.update_quantity("P102", 3)

        product = self.inventory.get_lowest_stock_product()

        self.assertEqual(product.product_id, "P102")
        self.assertEqual(product.quantity, 3)

    def test_delete_product(self):
        deleted_product = self.inventory.delete_product("P102")

        self.assertEqual(deleted_product.product_id, "P102")
        self.assertIsNone(
            self.inventory.find_product("P102")
        )

    def test_delete_missing_product_raises_error(self):
        with self.assertRaises(KeyError):
            self.inventory.delete_product("P999")

    def test_deleted_product_not_returned_by_category(self):
        self.inventory.delete_product("P102")

        products = self.inventory.get_products_by_category(
            "Electronics"
        )

        product_ids = {
            product.product_id
            for product in products
        }

        self.assertNotIn("P102", product_ids)

    def test_deleted_product_not_returned_by_price_tree(self):
        self.inventory.delete_product("P102")

        products = self.inventory.get_products_sorted_by_price()

        product_ids = {
            product.product_id
            for product in products
        }

        self.assertNotIn("P102", product_ids)

    def test_deleted_product_not_returned_by_heap(self):
        self.inventory.update_quantity("P102", 3)
        self.inventory.delete_product("P102")

        product = self.inventory.get_lowest_stock_product()

        self.assertEqual(product.product_id, "P104")


if __name__ == "__main__":
    unittest.main()