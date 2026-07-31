"""
benchmark.py

Performance benchmark for the Phase 2 Dynamic Inventory Management System.
"""

import random
import time
import tracemalloc

from inventory_manager import InventoryManager
from product import Product


def generate_products(size):
    """Generate a list of random products."""
    products = []

    for i in range(size):
        products.append(
            Product(
                product_id=f"P{i}",
                name=f"Product{i}",
                category=f"Category{i % 10}",
                price=random.uniform(10, 1000),
                quantity=random.randint(1, 100),
            )
        )

    return products


def benchmark(size):
    inventory = InventoryManager()
    products = generate_products(size)

    tracemalloc.start()

    # Insert benchmark
    start = time.perf_counter()

    for product in products:
        inventory.add_product(product)

    insert_time = time.perf_counter() - start

    # Search benchmark
    start = time.perf_counter()

    for product in products:
        inventory.find_product(product.product_id)

    search_time = time.perf_counter() - start

    # Price traversal benchmark
    start = time.perf_counter()

    inventory.get_products_sorted_by_price()

    traversal_time = time.perf_counter() - start

    # Lowest stock benchmark
    start = time.perf_counter()

    inventory.get_lowest_stock_product()

    heap_time = time.perf_counter() - start

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"\nDataset Size: {size}")
    print(f"Insertion Time       : {insert_time:.6f} sec")
    print(f"Search Time          : {search_time:.6f} sec")
    print(f"Traversal Time       : {traversal_time:.6f} sec")
    print(f"Lowest Stock Time    : {heap_time:.6f} sec")
    print(f"Peak Memory Usage    : {peak / (1024 * 1024):.2f} MB")


if __name__ == "__main__":
    random.seed(42)

    for size in [1000, 5000, 10000]:
        benchmark(size)
        