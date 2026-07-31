import unittest

from optimized_inventory_manager import OptimizedInventoryManager
from product import Product


class TestOptimizedInventoryManager(unittest.TestCase):

    def setUp(self):
        self.inventory = OptimizedInventoryManager()

        self.products = [
            Product("P101", "Keyboard", "Electronics", 50.00, 12),
            Product("P102", "Mouse", "Electronics", 20.00, 30),
            Product("P103", "Monitor", "Electronics", 200.00, 8),
            Product("P104", "Office Chair", "Furniture", 150.00, 5),
        ]

        self.inventory.add_products(self.products)

    def test_add_products(self):
        self.assertEqual(len(self.inventory.products), 4)

    def test_find_product(self):
        product = self.inventory.find_product("P101")
        self.assertEqual(product.name, "Keyboard")

    def test_duplicate_product_raises_error(self):
        duplicate = Product(
            "P101",
            "Duplicate",
            "Electronics",
            99.00,
            10,
        )

        with self.assertRaises(ValueError):
            self.inventory.add_product(duplicate)

    def test_products_sorted_by_price(self):
        products = self.inventory.get_products_sorted_by_price()
        prices = [product.price for product in products]

        self.assertEqual(prices, [20.00, 50.00, 150.00, 200.00])

    def test_equal_prices(self):
        product = Product(
            "P105",
            "Headphones",
            "Electronics",
            50.00,
            15,
        )

        self.inventory.add_product(product)

        product_ids = [
            item.product_id
            for item in self.inventory.get_products_sorted_by_price()
        ]

        self.assertIn("P101", product_ids)
        self.assertIn("P105", product_ids)

    def test_update_quantity(self):
        self.inventory.update_quantity("P102", 3)

        product = self.inventory.find_product("P102")
        self.assertEqual(product.quantity, 3)

    def test_lowest_stock_after_update(self):
        self.inventory.update_quantity("P102", 3)

        product = self.inventory.get_lowest_stock_product()
        self.assertEqual(product.product_id, "P102")

    def test_update_price(self):
        self.inventory.update_price("P101", 10.00)

        products = self.inventory.get_products_sorted_by_price()

        self.assertEqual(products[0].product_id, "P101")
        self.assertEqual(products[0].price, 10.00)

    def test_negative_price_update_raises_error(self):
        with self.assertRaises(ValueError):
            self.inventory.update_price("P101", -10.00)

    def test_delete_product(self):
        deleted = self.inventory.delete_product("P102")

        self.assertEqual(deleted.product_id, "P102")
        self.assertNotIn("P102", self.inventory.products)

    def test_deleted_product_removed_from_avl_tree(self):
        self.inventory.delete_product("P102")

        product_ids = [
            product.product_id
            for product in self.inventory.get_products_sorted_by_price()
        ]

        self.assertNotIn("P102", product_ids)

    def test_deleted_product_removed_from_category(self):
        self.inventory.delete_product("P102")

        product_ids = [
            product.product_id
            for product in self.inventory.get_products_by_category(
                "Electronics"
            )
        ]

        self.assertNotIn("P102", product_ids)

    def test_price_cache_invalidated_after_add(self):
        first_result = self.inventory.get_products_sorted_by_price()

        self.inventory.add_product(
            Product("P105", "Notebook", "Office", 5.00, 40)
        )

        second_result = self.inventory.get_products_sorted_by_price()

        self.assertEqual(first_result[0].product_id, "P102")
        self.assertEqual(second_result[0].product_id, "P105")

    def test_price_cache_invalidated_after_update(self):
        self.inventory.get_products_sorted_by_price()

        self.inventory.update_price("P103", 1.00)

        products = self.inventory.get_products_sorted_by_price()

        self.assertEqual(products[0].product_id, "P103")

    def test_price_cache_invalidated_after_delete(self):
        self.inventory.get_products_sorted_by_price()

        self.inventory.delete_product("P102")

        product_ids = [
            product.product_id
            for product in self.inventory.get_products_sorted_by_price()
        ]

        self.assertNotIn("P102", product_ids)

    def test_avl_tree_remains_balanced(self):
        self.assertTrue(self.inventory.is_price_tree_balanced())

        for index in range(105, 205):
            self.inventory.add_product(
                Product(
                    f"P{index}",
                    f"Product {index}",
                    "Stress",
                    float(index),
                    index,
                )
            )

        self.assertTrue(self.inventory.is_price_tree_balanced())

    def test_avl_tree_balanced_after_deletion(self):
        self.inventory.delete_product("P102")
        self.inventory.delete_product("P103")

        self.assertTrue(self.inventory.is_price_tree_balanced())

    def test_heap_compaction(self):
        for quantity in range(100):
            self.inventory.update_quantity("P101", quantity)

        maximum_size = (
            self.inventory.HEAP_REBUILD_FACTOR
            * len(self.inventory.products)
        )

        self.assertLessEqual(
            self.inventory.get_heap_size(),
            maximum_size,
        )

    def test_missing_product_raises_error(self):
        with self.assertRaises(ValueError):
            self.inventory.find_product("UNKNOWN")

    def test_empty_inventory_lowest_stock(self):
        inventory = OptimizedInventoryManager()

        self.assertIsNone(inventory.get_lowest_stock_product())


if __name__ == "__main__":
    unittest.main()