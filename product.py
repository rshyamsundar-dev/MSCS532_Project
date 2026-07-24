"""
product.py

Defines the Product class used in the Dynamic Inventory Management system.
"""


class Product:
    """Represents a single inventory product."""

    def __init__(self, product_id, name, category, price, quantity):
        if not product_id:
            raise ValueError("Product ID cannot be empty.")

        if price < 0:
            raise ValueError("Price cannot be negative.")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    def update_quantity(self, quantity):
        """Update the product quantity."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.quantity = quantity

    def __str__(self):
        return (
            f"Product("
            f"ID={self.product_id}, "
            f"Name={self.name}, "
            f"Category={self.category}, "
            f"Price=${self.price:.2f}, "
            f"Quantity={self.quantity})"
        )


