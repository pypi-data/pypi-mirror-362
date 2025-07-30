#!/usr/bin/env python3
"""
Debug why bulk is faster even for small arrays (100 data points)
"""
import numpy as np
import time
from ta_numba.trend import sma_numba

print("=== WHY BULK IS FASTER EVEN FOR SMALL ARRAYS ===")

# Test data
np.random.seed(42)
data_100 = np.random.rand(100) * 100 + 50
window = 20

# Warm up
_ = sma_numba(data_100)
print("🔥 JIT warmed up\n")

print("🔬 ANALYZING WHAT EACH APPROACH ACTUALLY DOES:")
print("=" * 70)

# 1. Bulk processing (what happens in one call)
print("1. BULK PROCESSING:")
start = time.perf_counter()
bulk_result = sma_numba(data_100)
bulk_time = time.perf_counter() - start
print(f"   - Single call to sma_numba(100 elements)")
print(f"   - Calculates 81 SMA values (positions 19-99)")
print(f"   - Time: {bulk_time*1000000:.2f}μs")
print(f"   - Last value: {bulk_result[-1]:.6f}")

# 2. Streaming simulation (what happens in loop)
print("\n2. STREAMING SIMULATION:")
streaming_data = list(data_100[:window])  # Start with first 20 elements
streaming_times = []

print(f"   - Starts with {window} elements")
print(f"   - Loops through remaining {100-window} elements")
print("   - Each iteration:")

total_streaming_time = 0
for i in range(window, 100):
    streaming_data.append(data_100[i])
    
    # This is what happens in each streaming update
    start = time.perf_counter()
    arr = np.array(streaming_data)  # Convert list to numpy
    result = sma_numba(arr)[-1]     # Calculate ALL SMAs, take last
    elapsed = time.perf_counter() - start
    
    streaming_times.append(elapsed)
    total_streaming_time += elapsed
    
    if i < window + 3:  # Show first few iterations
        print(f"     Iteration {i-window+1}: array size {len(streaming_data)}, time {elapsed*1000000:.2f}μs")

avg_streaming_time = total_streaming_time / (100 - window)
print(f"   - Total time: {total_streaming_time*1000000:.2f}μs")
print(f"   - Average per update: {avg_streaming_time*1000000:.2f}μs")
print(f"   - Last value: {result:.6f}")

print("\n🔬 DETAILED BREAKDOWN:")
print("=" * 70)

# Show exactly what sma_numba does for different array sizes
print("What sma_numba calculates for different array sizes:")
for size in [20, 25, 30, 50, 100]:
    test_data = data_100[:size]
    start = time.perf_counter()
    result = sma_numba(test_data)
    elapsed = time.perf_counter() - start
    
    num_smas = len(result)
    print(f"  Array size {size:>3}: calculates {num_smas:>2} SMAs in {elapsed*1000000:>6.2f}μs")

print("\n🔬 THE REAL PROBLEM:")
print("=" * 70)
print("Streaming approach does this 80 times:")
print("  - Convert list to numpy array")
print("  - Call sma_numba(array) → calculates ALL SMAs")
print("  - Take only the last value")
print("  - Throw away all other calculations")
print()
print("Total SMA calculations:")
print("  - Bulk: 81 SMAs (efficient)")
print("  - Streaming: 21+22+23+...+100 = 4,840 SMAs (wasteful!)")
print()

# Calculate total waste
total_calculations = sum(range(window+1, 101))
print(f"Streaming calculates {total_calculations} SMAs but only uses 80 of them")
print(f"Waste factor: {total_calculations/81:.1f}x more calculations than needed")

print("\n🚀 SOLUTION:")
print("=" * 70)
print("Use single-value functions that only calculate what you need:")

# Show optimized approach
from numba import njit

@njit
def sma_single(data, window):
    """Only calculate SMA for the last window"""
    if len(data) < window:
        return np.nan
    return np.mean(data[-window:])

# Warm up the optimized function
_ = sma_single(data_100, window)

# Test optimized streaming
streaming_data = list(data_100[:window])
optimized_times = []

total_optimized_time = 0
for i in range(window, 100):
    streaming_data.append(data_100[i])
    
    start = time.perf_counter()
    arr = np.array(streaming_data)
    result = sma_single(arr, window)  # Only calculate last SMA
    elapsed = time.perf_counter() - start
    
    optimized_times.append(elapsed)
    total_optimized_time += elapsed

avg_optimized_time = total_optimized_time / (100 - window)

print(f"Original streaming: {avg_streaming_time*1000000:.2f}μs per update")
print(f"Optimized streaming: {avg_optimized_time*1000000:.2f}μs per update")
print(f"Speedup: {avg_streaming_time/avg_optimized_time:.1f}x faster")
print(f"Bulk processing: {bulk_time*1000000:.2f}μs total")
print(f"Optimized streaming: {total_optimized_time*1000000:.2f}μs total")
print(f"Bulk vs optimized: {total_optimized_time/bulk_time:.1f}x slower (reasonable)")