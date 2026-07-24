"""
demo.py

Demonstrates the core functionality of the Dynamic Inventory Management
proof-of-concept application.
"""

from inventory_manager import InventoryManager
from product import Product


def print_section(title):
    """Print a formatted section heading."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def run_demo():
    """Run the inventory management demonstration."""
    inventory = InventoryManager()

    print_section("DYNAMIC INVENTORY MANAGEMENT SYSTEM")

    products = [
        Product("P101", "Keyboard", "Electronics", 50.00, 12),
        Product("P102", "Mouse", "Electronics", 20.00, 30),
        Product("P103", "Monitor", "Electronics", 200.00, 8),
        Product("P104", "Office Chair", "Furniture", 150.00, 5),
        Product("P105", "Notebook", "Office Supplies", 6.50, 40),
        Product("P106", "Desk Lamp", "Furniture", 35.00, 7),
    ]

    print_section("1. ADDING PRODUCTS")

    for product in products:
        inventory.add_product(product)
        print(f"Added: {product}")

    print_section("2. COMPLETE INVENTORY")
    inventory.display_inventory()

    print_section("3. SEARCHING BY PRODUCT ID")

    product = inventory.find_product("P103")

    if product is not None:
        print("Product found:")
        print(product)
    else:
        print("Product was not found.")

    print_section("4. CATEGORY-BASED RETRIEVAL")

    electronics = inventory.get_products_by_category("Electronics")

    for product in electronics:
        print(product)

    print_section("5. PRODUCTS SORTED BY PRICE")

    for product in inventory.get_products_sorted_by_price():
        print(product)

    print_section("6. LOWEST-STOCK PRODUCT")
    print(inventory.get_lowest_stock_product())

    print_section("7. QUANTITY UPDATE")

    print("Before update:")
    print(inventory.find_product("P102"))

    inventory.update_quantity("P102", 3)

    print("\nAfter update:")
    print(inventory.find_product("P102"))

    print("\nNew lowest-stock product:")
    print(inventory.get_lowest_stock_product())

    print_section("8. PRODUCT DELETION")

    deleted_product = inventory.delete_product("P102")
    print("Deleted:")
    print(deleted_product)

    print("\nLowest-stock product after deletion:")
    print(inventory.get_lowest_stock_product())

    print_section("9. ERROR HANDLING")

    try:
        inventory.add_product(
            Product("P101", "Duplicate Keyboard", "Electronics", 60.00, 10)
        )
    except ValueError as error:
        print("Duplicate product test:", error)

    try:
        inventory.update_quantity("P999", 10)
    except KeyError as error:
        print("Missing product test:", error)

    try:
        inventory.update_quantity("P103", -5)
    except ValueError as error:
        print("Negative quantity test:", error)

    print_section("DEMONSTRATION COMPLETED")


if __name__ == "__main__":
    run_demo()