#!/usr/bin/env python3
"""
Visualize exactly what the optimized streaming approach does
"""
import numpy as np
from ta_numba.trend import sma_numba

print("=== VISUALIZING OPTIMIZED STREAMING APPROACH ===")

# Simple example with 10 data points, SMA-3 window
data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
window = 3

print("🔬 STEP-BY-STEP STREAMING SIMULATION:")
print("=" * 60)

streaming_buffer = []  # This is our sliding window

for i, price in enumerate(data):
    print(f"\n📊 Tick {i+1}: New price = {price}")
    
    # Add new price to buffer
    streaming_buffer.append(price)
    
    # Keep only window size (sliding window)
    if len(streaming_buffer) > window:
        old_value = streaming_buffer.pop(0)  # Remove oldest
        print(f"   Buffer was full, removed oldest: {old_value}")
    
    print(f"   Current buffer: {streaming_buffer}")
    
    # Calculate SMA only if we have enough data
    if len(streaming_buffer) >= window:
        sma_value = sum(streaming_buffer) / len(streaming_buffer)
        print(f"   ✅ SMA-{window} = {sma_value:.1f}")
        
        # Show what single-value function does
        print(f"   💡 sma_numba_single(array={streaming_buffer}, window={window}) = {sma_value:.1f}")
    else:
        print(f"   ⏳ Not enough data yet (need {window}, have {len(streaming_buffer)})")

print("\n" + "=" * 60)
print("🔬 WHAT THE OPTIMIZED APPROACH DOES:")
print("=" * 60)

print("✅ EFFICIENT - Only keeps what's needed:")
print("   • Buffer size: CONSTANT (always ≤ window size)")
print("   • Memory usage: O(window) = O(3)")
print("   • Calculation: O(window) = O(3) per tick")
print("   • Total cost: O(n × window) = O(10 × 3) = O(30)")

print("\n❌ WASTEFUL - Keeps growing arrays:")
print("   • Array size: GROWING (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)")
print("   • Memory usage: O(n) = O(10) at the end")
print("   • Calculation: O(array_size) per tick")
print("   • Total cost: O(1+2+3+...+10) = O(55)")

print(f"\n📊 EFFICIENCY GAIN: {55/30:.1f}x less computation")

print("\n🔬 REAL EXAMPLE WITH OUR DATA:")
print("=" * 60)

# Show with actual ta-numba functions
from ta_numba.trend import sma_numba
from numba import njit

@njit
def sma_single(data, window):
    """Single value SMA - only calculate what we need"""
    return np.mean(data[-window:])

# Warm up
_ = sma_numba(np.array([1.0, 2.0, 3.0]))
_ = sma_single(np.array([1.0, 2.0, 3.0]), 3)

print("For 1000 data points, SMA-20:")

np.random.seed(42)
large_data = np.random.rand(1000) * 100 + 50

# Method 1: Optimized streaming (constant window size)
import time
streaming_buffer = []
start = time.perf_counter()

for price in large_data:
    streaming_buffer.append(price)
    if len(streaming_buffer) > 20:
        streaming_buffer.pop(0)  # Keep only last 20
    
    if len(streaming_buffer) >= 20:
        result = sma_single(np.array(streaming_buffer), 20)

optimized_time = time.perf_counter() - start

# Method 2: Wasteful streaming (growing arrays)
growing_buffer = []
start = time.perf_counter()

for price in large_data:
    growing_buffer.append(price)
    if len(growing_buffer) >= 20:
        result = sma_numba(np.array(growing_buffer))[-1]  # Calculate all, take last

wasteful_time = time.perf_counter() - start

# Method 3: Bulk processing
start = time.perf_counter()
bulk_result = sma_numba(large_data)
bulk_time = time.perf_counter() - start

print(f"✅ Optimized streaming: {optimized_time*1000:.2f}ms")
print(f"❌ Wasteful streaming:  {wasteful_time*1000:.2f}ms")
print(f"🚀 Bulk processing:     {bulk_time*1000:.2f}ms")

print(f"\nSpeedup: Optimized is {wasteful_time/optimized_time:.1f}x faster than wasteful")
print(f"Overhead: Optimized is {optimized_time/bulk_time:.1f}x slower than bulk")

print("\n💡 KEY INSIGHT:")
print("=" * 60)
print("The optimized approach is essentially:")
print("1. Maintain a sliding window of size = indicator period")
print("2. For each new tick:")
print("   - Add new value to window")
print("   - Remove oldest value if window > size")
print("   - Calculate indicator on current window only")
print("3. Never recalculate historical values")
print("\nThis is exactly what you'd do in real-time trading!")