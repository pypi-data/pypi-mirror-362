#!/usr/bin/env python3
"""
Deep dive into ta-numba performance vs pure numpy
"""
import numpy as np
import time
import os
from numba import njit

# Import ta-numba
from ta_numba.trend import sma_numba

def benchmark_operation(name, func, iterations=1000):
    """Benchmark a function over multiple iterations"""
    start = time.perf_counter()
    for _ in range(iterations):
        result = func()
    elapsed = time.perf_counter() - start
    avg_time = (elapsed / iterations) * 1000000  # microseconds
    print(f"{name:<40}: {avg_time:>8.2f}μs per call")
    return avg_time

# Test data
np.random.seed(42)
small_data = np.random.rand(20) * 100 + 50
window = 20

print("=== TA-NUMBA DEEP DIVE ANALYSIS ===")
print()

# Warm up ta-numba
print("Warming up ta-numba...")
_ = sma_numba(small_data, window)
print("Warm-up complete")
print()

print("🔬 COMPARING EQUIVALENT OPERATIONS:")
print("=" * 60)

# 1. ta-numba SMA function
benchmark_operation("ta-numba sma_numba(data, 20)", 
                   lambda: sma_numba(small_data, window))

# 2. What ta-numba is actually doing (from source code)
@njit(fastmath=True)
def manual_sma_njit(data, window):
    sma = np.full_like(data, np.nan)
    for i in range(len(data)):
        start_idx = max(0, i - window + 1)
        if i >= window - 1:  # Only calculate when we have enough data
            sma[i] = np.mean(data[start_idx:i+1])
    return sma

# Warm up
_ = manual_sma_njit(small_data, window)

benchmark_operation("Manual njit equivalent", 
                   lambda: manual_sma_njit(small_data, window))

# 3. Pure numpy equivalent (what it should be)
def pure_numpy_sma(data, window):
    result = np.full_like(data, np.nan)
    for i in range(window-1, len(data)):
        result[i] = np.mean(data[i-window+1:i+1])
    return result

benchmark_operation("Pure numpy (no JIT)", 
                   lambda: pure_numpy_sma(small_data, window))

# 4. Just the final window calculation
benchmark_operation("np.mean(final_window_only)", 
                   lambda: np.mean(small_data))

# 5. Pure Python equivalent  
def pure_python_sma(data, window):
    result = [np.nan] * len(data)
    for i in range(window-1, len(data)):
        window_data = data[i-window+1:i+1]
        result[i] = sum(window_data) / len(window_data)
    return np.array(result)

benchmark_operation("Pure Python equivalent", 
                   lambda: pure_python_sma(small_data, window))

print("\n🔬 TESTING SINGLE WINDOW CALCULATION:")
print("=" * 60)

# What happens when we just calculate one window?
single_window = small_data[:window]

@njit(fastmath=True) 
def njit_mean(data):
    return np.mean(data)

# Warm up
_ = njit_mean(single_window)

benchmark_operation("njit np.mean (single window)", 
                   lambda: njit_mean(single_window))

benchmark_operation("numpy np.mean (single window)", 
                   lambda: np.mean(single_window))

benchmark_operation("Python sum/len (single window)", 
                   lambda: sum(single_window) / len(single_window))

print("\n🔬 TESTING DIFFERENT DATA SIZES:")
print("=" * 60)

# Test with different sizes
sizes = [5, 20, 100, 10000]
for size in sizes:
    test_data = np.random.rand(size)
    
    # Warm up
    _ = sma_numba(test_data, min(size, 20))
    
    # Benchmark
    start = time.perf_counter()
    for _ in range(100):
        result = sma_numba(test_data, min(size, 20))
    elapsed = time.perf_counter() - start
    avg_time = (elapsed / 100) * 1000000
    
    print(f"ta-numba SMA (size {size:>4}): {avg_time:>8.2f}μs per call")

print("\n🔬 FUNCTION CALL OVERHEAD ANALYSIS:")
print("=" * 60)

# Test just function call overhead
@njit
def empty_njit():
    return np.array([1.0])

def empty_numpy():
    return np.array([1.0])

# Warm up
_ = empty_njit()

benchmark_operation("Empty @njit function", lambda: empty_njit())
benchmark_operation("Empty numpy function", lambda: empty_numpy())

print("\n📊 DIAGNOSIS:")
print("=" * 60)
print("If ta-numba is slower than pure numpy/Python, possible causes:")
print("1. JIT compilation overhead for small arrays")
print("2. Complex function internals (type checking, etc.)")  
print("3. Memory allocation patterns")
print("4. Loop overhead in ta-numba implementation")
print("5. Numba dispatch overhead")

# Test with JIT disabled
print("\n🔬 TESTING WITH JIT DISABLED:")
print("=" * 60)

# Save current environment
original_jit = os.environ.get('NUMBA_DISABLE_JIT', '0')
os.environ['NUMBA_DISABLE_JIT'] = '1'

# Need to reimport to disable JIT
import importlib
import ta_numba.trend
importlib.reload(ta_numba.trend)
from ta_numba.trend import sma_numba as sma_numba_no_jit

benchmark_operation("ta-numba (JIT disabled)", 
                   lambda: sma_numba_no_jit(small_data, window))

# Restore environment
os.environ['NUMBA_DISABLE_JIT'] = original_jit