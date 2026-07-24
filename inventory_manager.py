"""
inventory_manager.py

Integrates the data structures used by the Dynamic Inventory Management
proof-of-concept application.

Data structures:
1. Dictionary for product lookup by product ID
2. Binary Search Tree for price-based ordering
3. Min-heap for low-stock retrieval
4. Category map for category-based grouping
"""

import heapq

from product import Product
from price_tree import PriceTree


class InventoryManager:
    """Manages products using multiple coordinated data structures."""

    def __init__(self):
        # Hash table: product ID -> Product object
        self.products = {}

        # Category map: category -> set of product IDs
        self.categories = {}

        # Min-heap entries: (quantity, sequence_number, product_id)
        self.stock_heap = []

        # Prevents comparison errors when quantities are equal
        self.sequence_number = 0

        # Binary Search Tree for price ordering
        self.price_tree = PriceTree()

    def add_product(self, product):
        """Add a new product to all inventory data structures."""
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added.")

        if product.product_id in self.products:
            raise ValueError(
                f"Product ID '{product.product_id}' already exists."
            )

        # Add product to hash table
        self.products[product.product_id] = product

        # Add product ID to category map
        if product.category not in self.categories:
            self.categories[product.category] = set()

        self.categories[product.category].add(product.product_id)

        # Add product to the price tree
        self.price_tree.insert(product)

        # Add product to the min-heap
        self._push_to_heap(product)

    def _push_to_heap(self, product):
        """Insert the current product quantity into the min-heap."""
        heapq.heappush(
            self.stock_heap,
            (
                product.quantity,
                self.sequence_number,
                product.product_id
            )
        )

        self.sequence_number += 1

    def find_product(self, product_id):
        """Return a product using its unique ID."""
        return self.products.get(product_id)

    def update_quantity(self, product_id, new_quantity):
        """Update a product's quantity and refresh its heap entry."""
        product = self.find_product(product_id)

        if product is None:
            raise KeyError(f"Product ID '{product_id}' was not found.")

        product.update_quantity(new_quantity)

        # Add a new heap entry.
        # Older entries are ignored during retrieval.
        self._push_to_heap(product)

    def get_products_by_category(self, category):
        """Return all products belonging to a category."""
        product_ids = self.categories.get(category, set())

        return [
            self.products[product_id]
            for product_id in product_ids
            if product_id in self.products
        ]

    def get_lowest_stock_product(self):
        """Return the active product with the lowest quantity."""
        while self.stock_heap:
            quantity, _, product_id = self.stock_heap[0]

            product = self.products.get(product_id)

            # Remove entries belonging to deleted products
            if product is None:
                heapq.heappop(self.stock_heap)
                continue

            # Remove outdated quantity entries
            if product.quantity != quantity:
                heapq.heappop(self.stock_heap)
                continue

            return product

        return None

    def get_products_sorted_by_price(self):
        """Return all active products in ascending price order."""
        return [
            product
            for product in self.price_tree.inorder()
            if product.product_id in self.products
        ]

    def delete_product(self, product_id):
        """Delete a product from the active inventory."""
        product = self.find_product(product_id)

        if product is None:
            raise KeyError(f"Product ID '{product_id}' was not found.")

        # Remove from main product dictionary
        del self.products[product_id]

        # Remove from category map
        category_products = self.categories.get(product.category)

        if category_products is not None:
            category_products.discard(product_id)

            if not category_products:
                del self.categories[product.category]

        # Heap and price-tree entries remain physically present,
        # but inactive records are ignored during retrieval.
        return product

    def display_inventory(self):
        """Display all active products."""
        if not self.products:
            print("Inventory is empty.")
            return

        for product in self.products.values():
            print(product)

