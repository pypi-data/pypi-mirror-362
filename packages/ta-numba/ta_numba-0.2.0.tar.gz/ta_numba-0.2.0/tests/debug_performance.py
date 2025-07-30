#!/usr/bin/env python3
"""
Debug ta-numba vs pure Python performance
"""
import numpy as np
import time
from ta_numba.trend import sma_numba

# Test data
np.random.seed(42)
prices = np.random.rand(10000) * 100 + 50
window = 20

print("=== DEBUGGING ta-numba vs Pure Python ===")

# Warm up ta-numba
print("Warming up ta-numba...")
_ = sma_numba(prices[:100])
print("Warm-up complete")

# Test 1: Single ta-numba call on small window
print("\n1. Single ta-numba call on 20 values:")
small_data = prices[:window]
start = time.perf_counter()
result = sma_numba(small_data)
elapsed = time.perf_counter() - start
print(f"   ta-numba: {elapsed*1000000:.2f}μs")

# Test 2: Pure Python equivalent
print("\n2. Pure Python equivalent:")
start = time.perf_counter()
result_py = np.mean(small_data)
elapsed = time.perf_counter() - start
print(f"   np.mean: {elapsed*1000000:.2f}μs")

# Test 3: Manual Python loop
print("\n3. Manual Python sum/division:")
start = time.perf_counter()
total = sum(small_data)
result_manual = total / len(small_data)
elapsed = time.perf_counter() - start
print(f"   Manual: {elapsed*1000000:.2f}μs")

# Test 4: What's happening in my streaming approach
print("\n4. Simulating my bad streaming approach:")
values = []
total_time = 0
num_calls = 100

for i in range(num_calls):
    values.append(prices[i])
    if len(values) >= window:
        # This is what I'm doing in streaming
        start = time.perf_counter()
        window_data = np.array(values[-window:])  # Array creation
        result = sma_numba(window_data)           # Function call
        final_result = result[-1]                 # Extract result
        elapsed = time.perf_counter() - start
        total_time += elapsed

avg_time = (total_time / num_calls) * 1000000
print(f"   Bad streaming approach: {avg_time:.2f}μs per call")

# Test 5: Good streaming approach
print("\n5. Good streaming approach:")
class GoodSMA:
    def __init__(self, window):
        self.window = window
        self.values = []
        self.sum_val = 0.0
    
    def update(self, value):
        self.values.append(value)
        self.sum_val += value
        
        if len(self.values) > self.window:
            old = self.values.pop(0)
            self.sum_val -= old
        
        return self.sum_val / len(self.values) if len(self.values) == self.window else np.nan

good_sma = GoodSMA(window)
total_time = 0

for i in range(num_calls):
    start = time.perf_counter()
    result = good_sma.update(prices[i])
    elapsed = time.perf_counter() - start
    total_time += elapsed

avg_time = (total_time / num_calls) * 1000000
print(f"   Good streaming approach: {avg_time:.2f}μs per call")

# Test 6: Let's try disabling JIT
print("\n6. Testing with different approaches:")

# Array creation overhead
start = time.perf_counter()
for _ in range(1000):
    arr = np.array(prices[:window])
elapsed = time.perf_counter() - start
print(f"   Array creation (1000x): {(elapsed/1000)*1000000:.2f}μs per creation")

# Function call overhead  
data = np.array(prices[:window])
start = time.perf_counter()
for _ in range(1000):
    result = sma_numba(data)
elapsed = time.perf_counter() - start
print(f"   Function call (1000x): {(elapsed/1000)*1000000:.2f}μs per call")