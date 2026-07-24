"""
price_tree.py

Binary Search Tree implementation for organizing products by price.
"""

from product import Product


class TreeNode:
    """Represents a node in the Binary Search Tree."""

    def __init__(self, product):
        self.product = product
        self.left = None
        self.right = None


class PriceTree:
    """Binary Search Tree that stores products ordered by price."""

    def __init__(self):
        self.root = None

    def insert(self, product):
        """Insert a product into the tree."""
        if self.root is None:
            self.root = TreeNode(product)
        else:
            self._insert(self.root, product)

    def _insert(self, node, product):
        if product.price < node.product.price:
            if node.left is None:
                node.left = TreeNode(product)
            else:
                self._insert(node.left, product)
        else:
            if node.right is None:
                node.right = TreeNode(product)
            else:
                self._insert(node.right, product)

    def inorder(self):
        """Return products sorted by price."""
        products = []
        self._inorder(self.root, products)
        return products

    def _inorder(self, node, products):
        if node:
            self._inorder(node.left, products)
            products.append(node.product)
            self._inorder(node.right, products)

