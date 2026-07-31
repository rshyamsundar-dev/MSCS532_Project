import matplotlib.pyplot as plt

# Dataset sizes
sizes = [1000, 5000, 10000]

# Random dataset benchmark
phase2_insert = [0.003766, 0.019571, 0.065160]
phase3_insert = [0.011157, 0.068387, 0.147952]

phase2_memory = [0.39, 1.69, 3.18]
phase3_memory = [0.37, 1.84, 3.58]

# Stress-test benchmark
stress_phase2 = [0.077743, 1.464634, 5.723935]
stress_phase3 = [0.006865, 0.041423, 0.090211]

# Graph 1: Insertion Performance
plt.figure(figsize=(7, 5))
plt.plot(sizes, phase2_insert, marker="o", label="Phase 2")
plt.plot(sizes, phase3_insert, marker="o", label="Phase 3")
plt.xlabel("Dataset Size")
plt.ylabel("Insertion Time (seconds)")
plt.title("Insertion Performance Comparison")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("graph_insertion.png")
plt.close()

# Graph 2: Memory Usage
plt.figure(figsize=(7, 5))
plt.plot(sizes, phase2_memory, marker="o", label="Phase 2")
plt.plot(sizes, phase3_memory, marker="o", label="Phase 3")
plt.xlabel("Dataset Size")
plt.ylabel("Peak Memory (MB)")
plt.title("Memory Usage Comparison")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("graph_memory.png")
plt.close()

# Graph 3: Worst-Case Stress Test
plt.figure(figsize=(7, 5))
plt.plot(sizes, stress_phase2, marker="o", label="Phase 2 BST")
plt.plot(sizes, stress_phase3, marker="o", label="Phase 3 AVL")
plt.xlabel("Dataset Size")
plt.ylabel("Insertion Time (seconds)")
plt.title("Ascending-Order Stress Test")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("graph_stress_test.png")
plt.close()

print("Graphs created successfully.")