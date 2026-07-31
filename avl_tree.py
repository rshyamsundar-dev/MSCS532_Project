"""
avl_tree.py

Self-balancing AVL tree used to store products by price.
The key combines price and product ID so products with the same
price can still be stored uniquely.
"""


class AVLNode:
    """Represents one node in the AVL tree."""

    def __init__(self, product):
        self.product = product
        self.key = (product.price, product.product_id)
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """AVL tree supporting insertion, deletion, and in-order traversal."""

    def __init__(self):
        self.root = None

    def _height(self, node):
        """Return the height of a node."""
        if node is None:
            return 0

        return node.height

    def _update_height(self, node):
        """Recalculate a node's height."""
        node.height = 1 + max(
            self._height(node.left),
            self._height(node.right),
        )

    def _balance_factor(self, node):
        """Return the balance factor of a node."""
        if node is None:
            return 0

        return self._height(node.left) - self._height(node.right)

    def _rotate_right(self, unbalanced_node):
        """Perform a right rotation."""
        new_root = unbalanced_node.left
        transferred_subtree = new_root.right

        new_root.right = unbalanced_node
        unbalanced_node.left = transferred_subtree

        self._update_height(unbalanced_node)
        self._update_height(new_root)

        return new_root

    def _rotate_left(self, unbalanced_node):
        """Perform a left rotation."""
        new_root = unbalanced_node.right
        transferred_subtree = new_root.left

        new_root.left = unbalanced_node
        unbalanced_node.right = transferred_subtree

        self._update_height(unbalanced_node)
        self._update_height(new_root)

        return new_root

    def insert(self, product):
        """Insert a product into the AVL tree."""
        self.root = self._insert(self.root, product)

    def _insert(self, node, product):
        """Recursively insert and rebalance the tree."""
        if node is None:
            return AVLNode(product)

        product_key = (product.price, product.product_id)

        if product_key < node.key:
            node.left = self._insert(node.left, product)
        elif product_key > node.key:
            node.right = self._insert(node.right, product)
        else:
            node.product = product
            return node

        self._update_height(node)

        balance = self._balance_factor(node)

        # Left-left case
        if balance > 1 and product_key < node.left.key:
            return self._rotate_right(node)

        # Right-right case
        if balance < -1 and product_key > node.right.key:
            return self._rotate_left(node)

        # Left-right case
        if balance > 1 and product_key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right-left case
        if balance < -1 and product_key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def delete(self, price, product_id):
        """Delete a product using its price and product ID."""
        key = (price, product_id)
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        """Recursively delete a node and rebalance the tree."""
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right

            if node.right is None:
                return node.left

            successor = self._minimum_node(node.right)

            node.product = successor.product
            node.key = successor.key

            node.right = self._delete(node.right, successor.key)

        self._update_height(node)

        balance = self._balance_factor(node)

        # Left-left case
        if balance > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)

        # Left-right case
        if balance > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right-right case
        if balance < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)

        # Right-left case
        if balance < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _minimum_node(self, node):
        """Return the node with the smallest key."""
        current = node

        while current.left is not None:
            current = current.left

        return current

    def inorder(self):
        """Return all products in ascending price order."""
        products = []
        self._inorder(self.root, products)
        return products

    def _inorder(self, node, products):
        """Recursively perform an in-order traversal."""
        if node is None:
            return

        self._inorder(node.left, products)
        products.append(node.product)
        self._inorder(node.right, products)

    def is_balanced(self):
        """Return True when the entire AVL tree is balanced."""
        balanced, _ = self._check_balance(self.root)
        return balanced

    def _check_balance(self, node):
        """Validate AVL balance and stored node heights."""
        if node is None:
            return True, 0

        left_balanced, left_height = self._check_balance(node.left)
        right_balanced, right_height = self._check_balance(node.right)

        expected_height = 1 + max(left_height, right_height)

        balanced = (
            left_balanced
            and right_balanced
            and abs(left_height - right_height) <= 1
            and node.height == expected_height
        )

        return balanced, expected_height