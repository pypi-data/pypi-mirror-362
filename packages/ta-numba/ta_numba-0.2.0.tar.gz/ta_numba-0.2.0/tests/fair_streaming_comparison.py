#!/usr/bin/env python3
"""
Fair comparison of ta-numba vs pandas for streaming
"""
import numpy as np
import pandas as pd
import time
from ta_numba.trend import sma_numba

print("=== FAIR STREAMING COMPARISON ===")

# Test data
np.random.seed(42)
data = np.random.rand(1000) * 100 + 50
window = 20

# Warm up
_ = sma_numba(data[:window])
print("Warm-up complete\n")

print("🔬 APPLES TO APPLES COMPARISON:")
print("=" * 60)

def pandas_sma_single(series, period):
    """Pandas approach - only last value"""
    if len(series) < period:
        return np.nan
    return np.mean(series[-period:])

def ta_numba_sma_single(series, period=20):
    """ta-numba approach - only last value"""
    result = sma_numba(series)
    return result[-1] if len(result) > 0 else np.nan

def ta_numba_sma_last_window(series, period=20):
    """Optimized: Only calculate on last window"""
    if len(series) < period:
        return np.nan
    last_window = series[-period:]
    result = sma_numba(last_window)
    return result[-1]

# Test streaming scenario
streaming_data = []
results = {'pandas': [], 'ta_numba_full': [], 'ta_numba_window': []}
times = {'pandas': 0, 'ta_numba_full': 0, 'ta_numba_window': 0}

print("Testing streaming updates (100 → 500 ticks):")

for i in range(500):
    streaming_data.append(data[i])
    arr = np.array(streaming_data)
    
    if i >= 100:  # Start timing after initial fill
        # Pandas approach
        start = time.perf_counter()
        val1 = pandas_sma_single(arr, window)
        times['pandas'] += time.perf_counter() - start
        results['pandas'].append(val1)
        
        # ta-numba full array
        start = time.perf_counter()
        val2 = ta_numba_sma_single(arr, window)
        times['ta_numba_full'] += time.perf_counter() - start
        results['ta_numba_full'].append(val2)
        
        # ta-numba optimized (last window only)
        start = time.perf_counter()
        val3 = ta_numba_sma_last_window(arr, window)
        times['ta_numba_window'] += time.perf_counter() - start
        results['ta_numba_window'].append(val3)

num_updates = len(results['pandas'])

print(f"\nResults over {num_updates} streaming updates:")
print(f"{'Method':<25} | {'Total Time (ms)':<15} | {'μs per tick':<12} | {'Relative'}")
print("-" * 70)

pandas_time = times['pandas'] * 1000
pandas_per_tick = (times['pandas'] / num_updates) * 1000000

for method, total_time in times.items():
    total_ms = total_time * 1000
    per_tick = (total_time / num_updates) * 1000000
    relative = per_tick / pandas_per_tick
    
    print(f"{method:<25} | {total_ms:<15.2f} | {per_tick:<12.2f} | {relative:.2f}x")

# Verify results are the same
print("\n🔬 ACCURACY CHECK:")
print("=" * 60)
print("Comparing first 5 results:")
for i in range(5):
    p = results['pandas'][i]
    n1 = results['ta_numba_full'][i]
    n2 = results['ta_numba_window'][i]
    print(f"  pandas: {p:.6f}, ta_numba_full: {n1:.6f}, ta_numba_window: {n2:.6f}")

print("\n📊 WHAT THIS MEANS:")
print("=" * 60)
print("1. The original comparison was unfair:")
print("   - pandas: O(window) = O(20)")
print("   - ta-numba: O(array_size) = O(100→500)")
print()
print("2. When comparing apples to apples:")
print("   - Both calculate the same thing")
print("   - ta-numba's overhead becomes apparent")
print()
print("3. For streaming, the winner is:")
print("   - Simple operations (np.mean): Use direct calculation")
print("   - Complex operations (RSI, MACD): Use ta-numba")
print("   - True streaming: Use incremental algorithms")