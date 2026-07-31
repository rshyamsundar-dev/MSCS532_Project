"""
stress_test.py

Compares Phase 2 and Phase 3 using ascending prices.
Ascending input creates a worst-case unbalanced Phase 2 BST.
"""

import sys
import time

from inventory_manager import InventoryManager
from optimized_inventory_manager import OptimizedInventoryManager
from product import Product


# Allow deeper recursion so the Phase 2 recursive BST can be tested.
sys.setrecursionlimit(100000)


DATASET_SIZES = [1000, 5000, 10000]


def generate_ascending_products(size):
    """Generate products with strictly increasing prices."""
    return [
        Product(
            product_id=f"P{index:07d}",
            name=f"Product {index}",
            category=f"Category {index % 10}",
            price=float(index),
            quantity=(index % 100) + 1,
        )
        for index in range(size)
    ]


def clone_products(products):
    """Create independent products for each implementation."""
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


def measure_insertion(manager_class, products):
    inventory = manager_class()

    start = time.perf_counter()

    for product in products:
        inventory.add_product(product)

    elapsed = time.perf_counter() - start

    return inventory, elapsed


def main():
    print("\nASCENDING-PRICE STRESS TEST")
    print("-" * 72)

    for size in DATASET_SIZES:
        products = generate_ascending_products(size)

        phase2_inventory, phase2_time = measure_insertion(
            InventoryManager,
            clone_products(products),
        )

        phase3_inventory, phase3_time = measure_insertion(
            OptimizedInventoryManager,
            clone_products(products),
        )

        print(f"\nDataset size: {size}")
        print(f"Phase 2 insertion: {phase2_time:.6f} seconds")
        print(f"Phase 3 insertion: {phase3_time:.6f} seconds")
        print(
            "Phase 3 AVL balanced:",
            phase3_inventory.is_price_tree_balanced(),
        )

        if phase3_time > 0:
            print(
                f"Phase 2 / Phase 3 ratio: "
                f"{phase2_time / phase3_time:.2f}x"
            )


if __name__ == "__main__":
    main()