#!/usr/bin/env python3
"""
Debug why streaming is so slow - check if we're using the optimized approach.
"""

import numpy as np
import time
from ta_numba.trend import sma_numba
from ta_numba.streaming import SMAStreaming

def debug_streaming_performance():
    """Debug the streaming performance issue."""
    print("🔍 DEBUGGING STREAMING PERFORMANCE")
    print("=" * 50)
    
    # Generate test data
    np.random.seed(42)
    data_sizes = [1000, 5000, 10000]
    
    for size in data_sizes:
        print(f"\n📊 Testing {size:,} data points:")
        print("-" * 30)
        
        # Generate data
        prices = np.random.uniform(90, 110, size)
        
        # === BULK PROCESSING ===
        start = time.perf_counter()
        bulk_result = sma_numba(prices, 20)
        bulk_time = time.perf_counter() - start
        
        # === STREAMING PROCESSING (Current Implementation) ===
        sma_stream = SMAStreaming(20)
        start = time.perf_counter()
        streaming_results = []
        for price in prices:
            result = sma_stream.update(price)
            streaming_results.append(result)
        streaming_time = time.perf_counter() - start
        
        # === OPTIMIZED STREAMING (What we should have) ===
        from numba import njit
        
        @njit(fastmath=True)
        def sma_optimized_single(data: np.ndarray, window: int) -> float:
            """Only calculate SMA for the last window - single value output"""
            if len(data) < window:
                return np.nan
            return np.mean(data[-window:])
        
        # Warm up
        _ = sma_optimized_single(prices[:50], 20)
        
        # Test optimized streaming
        optimized_results = []
        streaming_data = []
        
        start = time.perf_counter()
        for price in prices:
            streaming_data.append(price)
            if len(streaming_data) > 20:
                streaming_data = streaming_data[-20:]  # Keep only last 20
            
            if len(streaming_data) >= 20:
                result = sma_optimized_single(np.array(streaming_data), 20)
                optimized_results.append(result)
            else:
                optimized_results.append(np.nan)
        optimized_time = time.perf_counter() - start
        
        # === RESULTS ===
        print(f"Bulk processing:        {bulk_time*1000:>8.2f}ms")
        print(f"Current streaming:      {streaming_time*1000:>8.2f}ms ({streaming_time/bulk_time:>5.1f}x slower)")
        print(f"Optimized streaming:    {optimized_time*1000:>8.2f}ms ({optimized_time/bulk_time:>5.1f}x slower)")
        print(f"Improvement:            {streaming_time/optimized_time:>5.1f}x faster")
        
        # Verify accuracy
        streaming_array = np.array(streaming_results)
        optimized_array = np.array(optimized_results)
        
        valid_mask = ~np.isnan(bulk_result)
        if np.sum(valid_mask) > 0:
            current_max_diff = np.max(np.abs(streaming_array[valid_mask] - bulk_result[valid_mask]))
            optimized_max_diff = np.max(np.abs(optimized_array[valid_mask] - bulk_result[valid_mask]))
            print(f"Current accuracy:       {current_max_diff:.2e} max diff")
            print(f"Optimized accuracy:     {optimized_max_diff:.2e} max diff")

def investigate_sma_streaming_implementation():
    """Look at what SMAStreaming is actually doing."""
    print("\n🔍 INVESTIGATING SMAStreaming IMPLEMENTATION")
    print("=" * 50)
    
    # Let's trace what happens in SMAStreaming
    sma_stream = SMAStreaming(20)
    
    # Check the buffer behavior
    test_data = [100, 101, 102, 103, 104]
    
    print("Tracing SMAStreaming updates:")
    for i, price in enumerate(test_data):
        result = sma_stream.update(price)
        print(f"Update {i+1}: price={price}, buffer_size={len(sma_stream.buffer)}, result={result}")
    
    # Add more data to see buffer behavior
    for i in range(20):
        price = 100 + i
        result = sma_stream.update(price)
        if i < 3 or i > 15:  # Show first few and last few
            print(f"Update {i+6}: price={price}, buffer_size={len(sma_stream.buffer)}, result={result:.2f}")
    
    print(f"\nFinal buffer size: {len(sma_stream.buffer)}")
    print(f"Buffer contents: {list(sma_stream.buffer)}")

def analyze_performance_bottlenecks():
    """Analyze where the performance bottleneck is."""
    print("\n🔍 ANALYZING PERFORMANCE BOTTLENECKS")
    print("=" * 50)
    
    # Test different aspects of the streaming process
    data = np.random.uniform(90, 110, 1000)
    
    # Test 1: Just the buffer operations
    from collections import deque
    buffer = deque(maxlen=20)
    
    start = time.perf_counter()
    for price in data:
        buffer.append(price)
        if len(buffer) >= 20:
            result = np.mean(buffer)
    buffer_time = time.perf_counter() - start
    
    # Test 2: Full SMAStreaming
    sma_stream = SMAStreaming(20)
    start = time.perf_counter()
    for price in data:
        result = sma_stream.update(price)
    streaming_time = time.perf_counter() - start
    
    # Test 3: Optimized approach
    streaming_data = []
    start = time.perf_counter()
    for price in data:
        streaming_data.append(price)
        if len(streaming_data) > 20:
            streaming_data = streaming_data[-20:]
        if len(streaming_data) >= 20:
            result = np.mean(streaming_data[-20:])
    optimized_time = time.perf_counter() - start
    
    print(f"Buffer operations only: {buffer_time*1000:>8.2f}ms")
    print(f"Full SMAStreaming:      {streaming_time*1000:>8.2f}ms")
    print(f"Optimized approach:     {optimized_time*1000:>8.2f}ms")
    print(f"Overhead factor:        {streaming_time/buffer_time:>8.1f}x")

if __name__ == "__main__":
    debug_streaming_performance()
    investigate_sma_streaming_implementation()
    analyze_performance_bottlenecks()
    
    print("\n🎯 CONCLUSION:")
    print("=" * 50)
    print("The current streaming implementation is not using the optimized approach!")
    print("We need to fix the streaming classes to use sliding windows efficiently.")
    print("Expected improvement: 5-20x faster streaming performance.")