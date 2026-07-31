# Dynamic Inventory Management System

## Overview

This project implements and optimizes a Dynamic Inventory Management System using Python data structures.

Phase 2 developed the proof-of-concept implementation using a dictionary, Binary Search Tree, min-heap, and category map.

Phase 3 improves scalability and worst-case performance through:

- A self-balancing AVL tree
- Physical AVL deletion
- Price-traversal caching
- Min-heap compaction
- Performance benchmarking
- Stress testing
- Automated validation

## Phase 3 Results

During the ascending-price stress test, the optimized AVL implementation inserted 10,000 products in 0.090211 seconds, compared with 5.723935 seconds for the original Binary Search Tree.

This represents an approximately 63.45× improvement under worst-case ordered input.

The optimized implementation also passed all 20 Phase 3 unit tests.

## Project Structure

- `product.py` – Product data model and validation
- `price_tree.py` – Original Phase 2 Binary Search Tree
- `inventory_manager.py` – Original Phase 2 inventory manager
- `avl_tree.py` – Optimized self-balancing AVL tree
- `optimized_inventory_manager.py` – Phase 3 optimized inventory manager
- `benchmark.py` – Phase 2 baseline benchmark
- `comparison_benchmark.py` – Phase 2 and Phase 3 comparison
- `stress_test.py` – Ascending-price stress test
- `test_inventory.py` – Phase 2 unit tests
- `test_optimized_inventory.py` – Phase 3 unit tests
- `generate_graphs.py` – Performance graph generator
- `comparison_results.csv` – Comparison benchmark results
- `stress_test_results.csv` – Stress-test results