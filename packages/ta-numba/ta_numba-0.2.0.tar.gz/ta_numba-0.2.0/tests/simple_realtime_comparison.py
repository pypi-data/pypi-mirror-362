#!/usr/bin/env python3
"""
Simple comparison of bulk vs streaming in a real-time scenario.
"""

import numpy as np
import time
from ta_numba.trend import sma_numba
from ta_numba.streaming import SMAStreaming

def simple_realtime_comparison():
    """Simple comparison showing the key difference."""
    print("🎯 SIMPLE REAL-TIME COMPARISON")
    print("=" * 50)
    
    # Parameters
    LOOKBACK_WINDOW = 1000  # How much history to keep
    NEW_TICKS = 500         # New ticks to process
    
    # Generate initial data
    np.random.seed(42)
    initial_data = np.random.uniform(95, 105, LOOKBACK_WINDOW)
    
    # Warm up JIT
    _ = sma_numba(initial_data, 20)
    sma_stream = SMAStreaming(20)
    for price in initial_data:
        sma_stream.update(price)
    
    print(f"Initial data: {LOOKBACK_WINDOW} points")
    print(f"New ticks to process: {NEW_TICKS}")
    print(f"SMA window: 20")
    print()
    
    # Track performance
    bulk_times = []
    streaming_times = []
    
    # Current data buffer for bulk processing
    data_buffer = list(initial_data)
    
    print("Processing new ticks...")
    for i in range(NEW_TICKS):
        # Generate new price tick
        new_price = data_buffer[-1] * (1 + np.random.normal(0, 0.01))
        
        # === BULK APPROACH ===
        # Add new tick to buffer
        data_buffer.append(new_price)
        if len(data_buffer) > LOOKBACK_WINDOW:
            data_buffer.pop(0)
        
        # Calculate SMA using entire buffer
        start = time.perf_counter()
        bulk_sma = sma_numba(np.array(data_buffer), 20)[-1]  # Only need last value
        bulk_time = time.perf_counter() - start
        bulk_times.append(bulk_time)
        
        # === STREAMING APPROACH ===
        # Update streaming indicator with just the new tick
        start = time.perf_counter()
        streaming_sma = sma_stream.update(new_price)
        streaming_time = time.perf_counter() - start
        streaming_times.append(streaming_time)
        
        # Verify they match
        if not np.isnan(bulk_sma) and not np.isnan(streaming_sma):
            assert abs(bulk_sma - streaming_sma) < 1e-10, f"Mismatch: {bulk_sma} vs {streaming_sma}"
        
        # Progress
        if (i + 1) % 100 == 0:
            print(f"  Processed {i+1} ticks...")
    
    # Results
    bulk_times_ms = np.array(bulk_times) * 1000
    streaming_times_ms = np.array(streaming_times) * 1000
    
    print(f"\n📊 RESULTS:")
    print(f"Bulk processing (recalculate entire array):")
    print(f"  Average: {np.mean(bulk_times_ms):.4f}ms per tick")
    print(f"  99th percentile: {np.percentile(bulk_times_ms, 99):.4f}ms")
    print(f"  Memory: {LOOKBACK_WINDOW * 8 / 1024:.1f} KB")
    print()
    print(f"Streaming processing (sliding window):")
    print(f"  Average: {np.mean(streaming_times_ms):.4f}ms per tick")
    print(f"  99th percentile: {np.percentile(streaming_times_ms, 99):.4f}ms")
    print(f"  Memory: ~160 bytes (constant)")
    print()
    
    speedup = np.mean(bulk_times_ms) / np.mean(streaming_times_ms)
    memory_savings = (LOOKBACK_WINDOW * 8) / 160
    
    print(f"✅ STREAMING ADVANTAGES:")
    print(f"  {speedup:.1f}x faster per tick")
    print(f"  {memory_savings:.0f}x less memory")
    print(f"  Constant latency regardless of history size")
    print(f"  Perfect for real-time applications")
    
    # Show scaling behavior
    print(f"\n📈 SCALING ANALYSIS:")
    print(f"As lookback window increases:")
    print(f"  Bulk: O(n) - linearly slower and more memory")
    print(f"  Streaming: O(1) - constant time and memory")
    print(f"  With 10,000 history: bulk ~10x slower, streaming unchanged")

if __name__ == "__main__":
    simple_realtime_comparison()