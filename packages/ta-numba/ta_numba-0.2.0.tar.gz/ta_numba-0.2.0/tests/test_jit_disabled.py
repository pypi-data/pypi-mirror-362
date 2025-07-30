#!/usr/bin/env python3
"""
Test ta-numba performance with JIT disabled
"""
import numpy as np
import time
import os

# Disable JIT compilation
os.environ['NUMBA_DISABLE_JIT'] = '1'

from ta_numba.trend import sma_numba

# Test data
np.random.seed(42)
prices = np.random.rand(10000) * 100 + 50
window = 20

print("=== ta-numba Performance with JIT DISABLED ===")

# Test 1: Single call
small_data = np.array(prices[:window])
start = time.perf_counter()
result = sma_numba(small_data)
elapsed = time.perf_counter() - start
print(f"1. Single ta-numba call (JIT disabled): {elapsed*1000000:.2f}μs")

# Test 2: Multiple calls
total_time = 0
num_calls = 100

for i in range(num_calls):
    start = time.perf_counter()
    result = sma_numba(np.array(prices[i:i+window]))
    elapsed = time.perf_counter() - start
    total_time += elapsed

avg_time = (total_time / num_calls) * 1000000
print(f"2. Average ta-numba call (JIT disabled): {avg_time:.2f}μs per call")

# Test 3: Compare with numpy
start = time.perf_counter()
for i in range(num_calls):
    result = np.mean(prices[i:i+window])
elapsed = time.perf_counter() - start
avg_numpy = (elapsed / num_calls) * 1000000
print(f"3. Average np.mean call: {avg_numpy:.2f}μs per call")

# Test 4: Pure Python
start = time.perf_counter()
for i in range(num_calls):
    window_data = prices[i:i+window]
    result = sum(window_data) / len(window_data)
elapsed = time.perf_counter() - start
avg_python = (elapsed / num_calls) * 1000000
print(f"4. Average pure Python: {avg_python:.2f}μs per call")

print(f"\nResults:")
print(f"ta-numba (no JIT): {avg_time:.2f}μs")
print(f"numpy: {avg_numpy:.2f}μs") 
print(f"Pure Python: {avg_python:.2f}μs")