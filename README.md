# Dynamic Inventory Management System

## Overview

This project is a proof-of-concept implementation of a Dynamic Inventory
Management System developed for Phase 2 of the course project.

The application demonstrates how multiple data structures can work together
to support common inventory operations such as insertion, searching, deletion,
category-based retrieval, price ordering, and low-stock identification.

## Data Structures

The project uses the following data structures:

- **Dictionary:** Stores products by unique product ID for efficient lookup.
- **Binary Search Tree:** Stores products by price and supports ascending-order traversal.
- **Min-Heap:** Identifies the product with the lowest available quantity.
- **Category Map:** Groups product IDs by product category.

## Project Structure

```
Dynamic-Inventory-Management/
├── product.py
├── price_tree.py
├── inventory_manager.py
├── demo.py
├── test_inventory.py
└── README.md