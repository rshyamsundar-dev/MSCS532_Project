"""
comparison_benchmark.py

Compares the Phase 2 inventory manager with the optimized Phase 3 manager.
"""

import csv
import random
import time
import tracemalloc

from inventory_manager import InventoryManager
from optimized_inventory_manager import OptimizedInventoryManager
from product import Product


DATASET_SIZES = [1000, 5000, 10000]
OUTPUT_FILE = "comparison_results.csv"


def generate_products(size):
    """Create deterministic product data for fair comparisons."""
    random.seed(42 + size)

    return [
        Product(
            product_id=f"P{index:07d}",
            name=f"Product {index}",
            category=f"Category {index % 10}",
            price=round(random.uniform(1.0, 1000.0), 2),
            quantity=random.randint(0, 1000),
        )
        for index in range(size)
    ]


def clone_products(products):
    """Create fresh Product objects for each implementation."""
    return [
        Product(
            product.product_id,
            product.name,
            product.category,
            product.price,
            product.quantity,
        )
        for product in products
    ]


def benchmark_manager(manager_class, products):
    """Measure one inventory-manager implementation."""
    inventory = manager_class()

    tracemalloc.start()

    start = time.perf_counter()
    for product in products:
        inventory.add_product(product)
    insertion_time = time.perf_counter() - start

    lookup_ids = [
        products[index].product_id
        for index in range(0, len(products), max(1, len(products) // 1000))
    ][:1000]

    start = time.perf_counter()
    for product_id in lookup_ids:
        inventory.find_product(product_id)
    search_time = time.perf_counter() - start

    start = time.perf_counter()
    inventory.get_products_sorted_by_price()
    first_traversal_time = time.perf_counter() - start

    start = time.perf_counter()
    inventory.get_products_sorted_by_price()
    repeated_traversal_time = time.perf_counter() - start

    start = time.perf_counter()
    inventory.get_lowest_stock_product()
    lowest_stock_time = time.perf_counter() - start

    current_memory, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "insertion_time": insertion_time,
        "search_time": search_time,
        "first_traversal_time": first_traversal_time,
        "repeated_traversal_time": repeated_traversal_time,
        "lowest_stock_time": lowest_stock_time,
        "peak_memory_mb": peak_memory / (1024 * 1024),
    }


def main():
    rows = []

    for size in DATASET_SIZES:
        print(f"\nTesting dataset size: {size}")

        source_products = generate_products(size)

        phase2_result = benchmark_manager(
            InventoryManager,
            clone_products(source_products),
        )

        phase3_result = benchmark_manager(
            OptimizedInventoryManager,
            clone_products(source_products),
        )

        for version, result in [
            ("Phase 2", phase2_result),
            ("Phase 3", phase3_result),
        ]:
            row = {
                "dataset_size": size,
                "version": version,
                **result,
            }
            rows.append(row)

            print(
                f"{version}: "
                f"insert={result['insertion_time']:.6f}s, "
                f"search={result['search_time']:.6f}s, "
                f"first traversal={result['first_traversal_time']:.6f}s, "
                f"repeated traversal={result['repeated_traversal_time']:.6f}s, "
                f"lowest stock={result['lowest_stock_time']:.6f}s, "
                f"memory={result['peak_memory_mb']:.2f} MB"
            )

    fieldnames = [
        "dataset_size",
        "version",
        "insertion_time",
        "search_time",
        "first_traversal_time",
        "repeated_traversal_time",
        "lowest_stock_time",
        "peak_memory_mb",
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nResults saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()