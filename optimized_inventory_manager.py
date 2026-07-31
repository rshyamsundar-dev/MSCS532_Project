"""
optimized_inventory_manager.py

Optimized inventory manager for Phase 3.

Optimizations:
1. Self-balancing AVL tree for price ordering.
2. Physical deletion from the AVL tree.
3. Periodic heap compaction to control stale entries.
4. Cached price traversal results.
"""

import heapq

from avl_tree import AVLTree
from product import Product


class OptimizedInventoryManager:
    """Coordinates optimized inventory data structures."""

    HEAP_REBUILD_FACTOR = 2

    def __init__(self):
        self.products = {}
        self.categories = {}
        self.stock_heap = []
        self.sequence_number = 0
        self.price_tree = AVLTree()

        # Cached result of the most recent price traversal.
        self._price_cache = None

    def add_product(self, product):
        """Add a product to all inventory data structures."""
        if not isinstance(product, Product):
            raise TypeError("product must be an instance of Product")

        if product.product_id in self.products:
            raise ValueError(
                f"Product ID '{product.product_id}' already exists."
            )

        self.products[product.product_id] = product

        if product.category not in self.categories:
            self.categories[product.category] = set()

        self.categories[product.category].add(product.product_id)

        self.price_tree.insert(product)
        self._push_to_heap(product)

        self._invalidate_price_cache()

    def add_products(self, products):
        """Add several products to the inventory."""
        for product in products:
            self.add_product(product)

    def _push_to_heap(self, product):
        """Insert the current product quantity into the stock heap."""
        self.sequence_number += 1

        heapq.heappush(
            self.stock_heap,
            (
                product.quantity,
                self.sequence_number,
                product.product_id,
            ),
        )

    def find_product(self, product_id):
        """Return a product by ID."""
        if product_id not in self.products:
            raise ValueError(f"Product ID '{product_id}' was not found.")

        return self.products[product_id]

    def update_quantity(self, product_id, new_quantity):
        """Update product quantity and add a fresh heap entry."""
        product = self.find_product(product_id)

        product.update_quantity(new_quantity)
        self._push_to_heap(product)

        self._compact_heap_if_needed()

        return product

    def update_price(self, product_id, new_price):
        """Update a product price while maintaining AVL ordering."""
        if new_price < 0:
            raise ValueError("Price cannot be negative.")

        product = self.find_product(product_id)
        old_price = product.price

        # Physically remove the old price-tree entry.
        self.price_tree.delete(old_price, product.product_id)

        product.price = new_price

        # Insert the product using its new price.
        self.price_tree.insert(product)

        self._invalidate_price_cache()

        return product

    def delete_product(self, product_id):
        """Physically remove a product from active structures."""
        product = self.find_product(product_id)

        # Remove from the AVL tree before removing the main record.
        self.price_tree.delete(product.price, product.product_id)

        del self.products[product_id]

        category_ids = self.categories.get(product.category)

        if category_ids is not None:
            category_ids.discard(product_id)

            if not category_ids:
                del self.categories[product.category]

        # Stale heap entries are removed during retrieval or compaction.
        self._compact_heap_if_needed()
        self._invalidate_price_cache()

        return product

    def get_products_by_category(self, category):
        """Return active products belonging to a category."""
        product_ids = self.categories.get(category, set())

        return [
            self.products[product_id]
            for product_id in product_ids
            if product_id in self.products
        ]

    def get_products_sorted_by_price(self):
        """Return products in ascending price order using a cache."""
        if self._price_cache is None:
            self._price_cache = self.price_tree.inorder()

        # Return a copy so callers cannot modify the stored cache.
        return list(self._price_cache)

    def get_lowest_stock_product(self):
        """Return the active product with the smallest quantity."""
        while self.stock_heap:
            quantity, _, product_id = self.stock_heap[0]

            product = self.products.get(product_id)

            if product is None or product.quantity != quantity:
                heapq.heappop(self.stock_heap)
                continue

            return product

        return None

    def _compact_heap_if_needed(self):
        """Rebuild the heap when stale entries become excessive."""
        active_count = len(self.products)

        if active_count == 0:
            self.stock_heap.clear()
            return

        maximum_size = self.HEAP_REBUILD_FACTOR * active_count

        if len(self.stock_heap) > maximum_size:
            self._rebuild_stock_heap()

    def _rebuild_stock_heap(self):
        """Rebuild the heap using only current product quantities."""
        self.stock_heap = []
        self.sequence_number = 0

        for product in self.products.values():
            self._push_to_heap(product)

    def _invalidate_price_cache(self):
        """Clear cached traversal results after tree modification."""
        self._price_cache = None

    def display_inventory(self):
        """Display all active products."""
        if not self.products:
            print("Inventory is empty.")
            return

        for product in self.products.values():
            print(product)

    def get_heap_size(self):
        """Return the current heap size for testing and analysis."""
        return len(self.stock_heap)

    def is_price_tree_balanced(self):
        """Return whether the AVL price tree is balanced."""
        return self.price_tree.is_balanced()