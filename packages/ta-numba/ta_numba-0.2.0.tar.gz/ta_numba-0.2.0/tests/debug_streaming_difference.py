#!/usr/bin/env python3
"""
Debug why ta-numba is fast on fixed arrays but slow in streaming
"""
import numpy as np
import time
from ta_numba.trend import sma_numba

print("=== DEBUGGING STREAMING vs FIXED ARRAY PERFORMANCE ===")

# Test data
np.random.seed(42)
data_20 = np.random.rand(20) * 100 + 50
data_100 = np.random.rand(100) * 100 + 50
data_1000 = np.random.rand(1000) * 100 + 50

# Warm up
_ = sma_numba(data_20)
print("Warm-up complete\n")

print("🔬 FIXED ARRAY TESTS (what ta_numba_deep_dive.py does):")
print("=" * 60)

# Test on fixed arrays
def benchmark_fixed(name, data, iterations=1000):
    start = time.perf_counter()
    for _ in range(iterations):
        result = sma_numba(data)
    elapsed = time.perf_counter() - start
    avg_time = (elapsed / iterations) * 1000000
    print(f"{name:<30}: {avg_time:>8.2f}μs per call")
    return avg_time

benchmark_fixed("sma_numba(20 elements)", data_20)
benchmark_fixed("sma_numba(100 elements)", data_100)
benchmark_fixed("sma_numba(1000 elements)", data_1000)

print("\n🔬 STREAMING TESTS (what ta-numba_comparison.py does):")
print("=" * 60)

# Simulate streaming - arrays grow over time
streaming_data = []
window = 20

# Pre-fill with initial data
for i in range(window):
    streaming_data.append(data_1000[i])

print("Testing streaming updates (arrays grow each tick):")

# Test different streaming sizes
test_sizes = [50, 100, 500, 1000]

for size in test_sizes:
    streaming_data = list(data_1000[:window])  # Reset
    
    start = time.perf_counter()
    for i in range(window, size):
        # Append new tick
        streaming_data.append(data_1000[i])
        
        # Convert to numpy and calculate (this is what the comparison does)
        close_np = np.array(streaming_data, dtype=float)
        result = sma_numba(close_np)
        
    elapsed = time.perf_counter() - start
    avg_time = (elapsed / (size - window)) * 1000000
    
    print(f"  Stream to size {size:>4}: {avg_time:>8.2f}μs per tick (array size: {len(streaming_data)})")

print("\n🔬 ANALYZING THE PROBLEM:")
print("=" * 60)

# What's the actual overhead?
streaming_list = list(data_1000[:100])

# 1. List to numpy conversion
start = time.perf_counter()
for _ in range(1000):
    arr = np.array(streaming_list, dtype=float)
elapsed = time.perf_counter() - start
print(f"np.array() conversion (100 elem): {(elapsed/1000)*1000000:.2f}μs")

# 2. ta-numba on growing arrays
print("\nta-numba cost on different array sizes:")
for size in [20, 50, 100, 200, 500, 1000]:
    test_array = np.random.rand(size)
    _ = sma_numba(test_array)  # Warm up
    
    start = time.perf_counter()
    for _ in range(100):
        result = sma_numba(test_array)
    elapsed = time.perf_counter() - start
    avg_time = (elapsed / 100) * 1000000
    
    print(f"  sma_numba({size:>4} elements): {avg_time:>8.2f}μs")

print("\n📊 CONCLUSION:")
print("=" * 60)
print("ta-numba gets slower as arrays grow because:")
print("1. It calculates SMA for EVERY position in the array")
print("2. Streaming tests have growing arrays (20→1000 elements)")
print("3. Cost increases linearly with array size")
print()
print("For a 1000-element array:")
print("- ta-numba calculates 1000 SMAs")
print("- We only need the last one!")
print("- 99.9% of computation is wasted")

# Compare approaches
print("\n🔬 OPTIMAL vs WASTEFUL:")
print("=" * 60)

test_array = np.random.rand(1000)

# Wasteful: Calculate all SMAs
start = time.perf_counter()
full_result = sma_numba(test_array)
last_value = full_result[-1]
elapsed1 = time.perf_counter() - start

# Optimal: Just calculate last window
start = time.perf_counter()
last_window = test_array[-20:]
optimal_result = np.mean(last_window)
elapsed2 = time.perf_counter() - start

print(f"Wasteful (full sma_numba): {elapsed1*1000000:.2f}μs")
print(f"Optimal (mean of last 20): {elapsed2*1000000:.2f}μs")
print(f"Waste factor: {elapsed1/elapsed2:.1f}x")