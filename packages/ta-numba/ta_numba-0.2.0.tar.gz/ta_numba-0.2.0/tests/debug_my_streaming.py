#!/usr/bin/env python3
"""
Debug my streaming implementation to find the real bottleneck
"""
import numpy as np
import time
from ta_numba.trend import sma_numba

# Recreate my bad streaming implementation
class MyBadStreamingTANumbaSMA:
    """ACTUAL ta-numba streaming using JIT-compiled function with incremental calculation"""
    
    def __init__(self, window: int):
        self.window = window
        self.values = []
        # Pre-compile the function with warm-up
        dummy = np.array([1.0, 2.0, 3.0])
        _ = sma_numba(dummy)  # Ensure JIT compilation
        
    def update(self, value: float) -> float:
        self.values.append(value)
        
        if len(self.values) >= self.window:
            if len(self.values) > self.window * 2:  # Prevent unbounded growth
                self.values = self.values[-self.window:]
            
            # Use actual ta-numba function on current window
            result = sma_numba(np.array(self.values[-self.window:]))
            return result[-1] if len(result) > 0 else np.nan
        
        return np.nan

# Good streaming implementation
class GoodStreamingSMA:
    def __init__(self, window: int):
        self.window = window
        self.values = []
        self.sum_val = 0.0
        
    def update(self, value: float) -> float:
        self.values.append(value)
        self.sum_val += value
        
        if len(self.values) > self.window:
            old_val = self.values.pop(0)
            self.sum_val -= old_val
            
        return self.sum_val / len(self.values) if len(self.values) == self.window else np.nan

# Optimized ta-numba streaming
class OptimizedTANumbaStreaming:
    def __init__(self, window: int):
        self.window = window
        self.values = []
        
        # Pre-allocate array to avoid recreation
        self.data_array = np.zeros(window)
        
        # Warm up
        _ = sma_numba(self.data_array)
        
    def update(self, value: float) -> float:
        self.values.append(value)
        
        if len(self.values) >= self.window:
            # Copy data to pre-allocated array (avoid np.array creation)
            window_data = self.values[-self.window:]
            self.data_array[:] = window_data
            
            # Call ta-numba on just final window
            result = sma_numba(self.data_array)
            return result[-1]
        
        return np.nan

print("=== DEBUGGING MY STREAMING IMPLEMENTATIONS ===")

# Test data
np.random.seed(42)
prices = np.random.rand(1000) * 100 + 50
window = 20

# Initialize
bad_sma = MyBadStreamingTANumbaSMA(window)
good_sma = GoodStreamingSMA(window)
opt_sma = OptimizedTANumbaStreaming(window)

# Pre-fill with some data
for i in range(window):
    bad_sma.update(prices[i])
    good_sma.update(prices[i])
    opt_sma.update(prices[i])

print("\n🔬 TIMING SINGLE UPDATE OPERATIONS:")
print("=" * 50)

def time_single_update(sma_obj, value):
    start = time.perf_counter()
    result = sma_obj.update(value)
    elapsed = time.perf_counter() - start
    return elapsed * 1000000  # microseconds

# Test multiple updates
iterations = 100
test_value = 75.0

# My bad implementation
total_time = 0
for _ in range(iterations):
    total_time += time_single_update(bad_sma, test_value)
print(f"My Bad ta-numba Streaming: {total_time/iterations:.2f}μs per update")

# Good implementation  
total_time = 0
for _ in range(iterations):
    total_time += time_single_update(good_sma, test_value)
print(f"Good Pure Python Streaming: {total_time/iterations:.2f}μs per update")

# Optimized implementation
total_time = 0
for _ in range(iterations):
    total_time += time_single_update(opt_sma, test_value)
print(f"Optimized ta-numba Streaming: {total_time/iterations:.2f}μs per update")

print("\n🔬 BREAKING DOWN THE BAD IMPLEMENTATION:")
print("=" * 50)

# Test components separately
window_data = prices[:window]

# 1. Array creation
start = time.perf_counter()
for _ in range(1000):
    arr = np.array(window_data)
elapsed = time.perf_counter() - start
print(f"np.array() creation: {(elapsed/1000)*1000000:.2f}μs per call")

# 2. ta-numba call on pre-created array
test_array = np.array(window_data)
start = time.perf_counter()
for _ in range(1000):
    result = sma_numba(test_array)
elapsed = time.perf_counter() - start
print(f"sma_numba() call: {(elapsed/1000)*1000000:.2f}μs per call")

# 3. List slicing
values_list = prices[:50].tolist()
start = time.perf_counter()
for _ in range(1000):
    sliced = values_list[-window:]
elapsed = time.perf_counter() - start
print(f"List slicing [-window:]: {(elapsed/1000)*1000000:.2f}μs per call")

# 4. Array indexing
start = time.perf_counter()
for _ in range(1000):
    result = test_array[-1]
elapsed = time.perf_counter() - start
print(f"Array indexing [-1]: {(elapsed/1000)*1000000:.2f}μs per call")

print("\n📊 TOTAL OVERHEAD PER UPDATE:")
print("=" * 50)
print("My bad implementation per update:")
print("  1. List append: ~0.01μs")
print("  2. List slicing: ~0.02μs") 
print("  3. Array creation: ~0.23μs")
print("  4. ta-numba call: ~0.69μs")
print("  5. Array indexing: ~0.001μs")
print("  TOTAL: ~0.95μs (but measured 20+μs!)")
print()
print("Something else is wrong...")

# Let's test the actual measured performance
print("\n🔬 ACTUAL MEASURED PERFORMANCE:")
print("=" * 50)

# Simulate what happens in the benchmark
streaming_prices = np.random.rand(100) * 100 + 50

# My implementation
bad_impl = MyBadStreamingTANumbaSMA(20)
start = time.time()
for price in streaming_prices:
    _ = bad_impl.update(price)
bad_time = time.time() - start
print(f"Bad implementation (100 ticks): {(bad_time/100)*1000000:.2f}μs per tick")

# Good implementation
good_impl = GoodStreamingSMA(20)  
start = time.time()
for price in streaming_prices:
    _ = good_impl.update(price)
good_time = time.time() - start
print(f"Good implementation (100 ticks): {(good_time/100)*1000000:.2f}μs per tick")