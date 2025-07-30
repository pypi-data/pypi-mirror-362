#!/usr/bin/env python3
"""
Investigate why the benchmark shows different performance than our debug test.
"""

import numpy as np
import time
from ta_numba.trend import sma_numba
from ta_numba.streaming import SMAStreaming

def investigate_benchmark_discrepancy():
    """Find out why benchmark shows different performance."""
    print("🔍 INVESTIGATING BENCHMARK DISCREPANCY")
    print("=" * 50)
    
    # Generate the SAME data as the benchmark
    np.random.seed(42)
    n_points = 1000
    
    # Generate realistic price series (like the benchmark does)
    base_price = 100.0
    prices = [base_price]
    
    for i in range(1, n_points):
        # Add some auto-correlation and volatility clustering
        prev_change = 0 if i == 1 else (prices[-1] - prices[-2]) / prices[-2]
        trend = 0.0001 + 0.1 * prev_change
        volatility = 0.015 + 0.5 * abs(prev_change)
        
        change = np.random.normal(trend, volatility)
        new_price = prices[-1] * (1 + change)
        prices.append(max(new_price, 0.01))
    
    close = np.array(prices)
    
    print(f"Generated {len(close)} data points")
    print(f"Data range: {close.min():.2f} to {close.max():.2f}")
    
    # === Test 1: Bulk processing (with warm-up) ===
    # Warm up
    _ = sma_numba(close[:100], 20)
    
    start = time.perf_counter()
    bulk_result = sma_numba(close, 20)
    bulk_time = time.perf_counter() - start
    
    print(f"\nBulk processing: {bulk_time*1000:.2f}ms")
    print(f"Bulk result shape: {bulk_result.shape}")
    print(f"Bulk result sample: {bulk_result[-5:]}")
    
    # === Test 2: Streaming processing (with warm-up) ===
    # Warm up
    warm_stream = SMAStreaming(20)
    for price in close[:50]:
        warm_stream.update(price)
    
    # Actual test
    sma_stream = SMAStreaming(20)
    start = time.perf_counter()
    streaming_results = []
    for price in close:
        result = sma_stream.update(price)
        streaming_results.append(result)
    streaming_time = time.perf_counter() - start
    
    print(f"\nStreaming processing: {streaming_time*1000:.2f}ms")
    print(f"Streaming results length: {len(streaming_results)}")
    print(f"Streaming result sample: {streaming_results[-5:]}")
    
    # === Test 3: Check what the benchmark is actually doing ===
    # Simulate the benchmark exactly
    def simulate_benchmark_method():
        """Simulate exactly what the benchmark does."""
        
        # Generate data like benchmark
        np.random.seed(42)
        base_price = 100.0
        prices = [base_price]
        
        for i in range(1, n_points):
            prev_change = 0 if i == 1 else (prices[-1] - prices[-2]) / prices[-2]
            trend = 0.0001 + 0.1 * prev_change
            volatility = 0.015 + 0.5 * abs(prev_change)
            
            change = np.random.normal(trend, volatility)
            new_price = prices[-1] * (1 + change)
            prices.append(max(new_price, 0.01))
        
        close = np.array(prices)
        
        # Warm up (like benchmark)
        warmup_data = close[:100]
        _ = sma_numba(warmup_data, 20)
        
        warm_stream = SMAStreaming(20)
        for price in warmup_data:
            warm_stream.update(price)
        
        # Bulk test
        start = time.perf_counter()
        bulk_result = sma_numba(close, 20)
        bulk_time = time.perf_counter() - start
        
        # Streaming test
        streaming_indicator = SMAStreaming(20)
        start = time.perf_counter()
        streaming_results = []
        for price in close:
            result = streaming_indicator.update(price)
            streaming_results.append(result)
        streaming_time = time.perf_counter() - start
        
        return bulk_time, streaming_time, bulk_result, streaming_results
    
    bulk_time_bench, streaming_time_bench, bulk_result_bench, streaming_results_bench = simulate_benchmark_method()
    
    print(f"\n📊 BENCHMARK SIMULATION:")
    print(f"Bulk time: {bulk_time_bench*1000:.2f}ms")
    print(f"Streaming time: {streaming_time_bench*1000:.2f}ms")
    print(f"Performance ratio: {streaming_time_bench/bulk_time_bench:.1f}x")
    
    # === Test 4: Check if it's the JIT compilation ===
    print(f"\n🔥 JIT COMPILATION CHECK:")
    
    # Test bulk multiple times
    bulk_times = []
    for i in range(5):
        start = time.perf_counter()
        _ = sma_numba(close, 20)
        bulk_times.append(time.perf_counter() - start)
    
    print(f"Bulk times: {[t*1000 for t in bulk_times]}")
    print(f"Bulk avg: {np.mean(bulk_times)*1000:.2f}ms")
    
    # Test streaming multiple times
    streaming_times = []
    for i in range(5):
        sma_stream = SMAStreaming(20)
        start = time.perf_counter()
        for price in close:
            sma_stream.update(price)
        streaming_times.append(time.perf_counter() - start)
    
    print(f"Streaming times: {[t*1000 for t in streaming_times]}")
    print(f"Streaming avg: {np.mean(streaming_times)*1000:.2f}ms")
    
    # === Test 5: Check the actual accuracy ===
    print(f"\n🎯 ACCURACY CHECK:")
    
    streaming_array = np.array(streaming_results)
    
    # Find valid indices
    valid_bulk = ~np.isnan(bulk_result)
    valid_streaming = ~np.isnan(streaming_array)
    valid_both = valid_bulk & valid_streaming
    
    print(f"Valid bulk values: {np.sum(valid_bulk)}")
    print(f"Valid streaming values: {np.sum(valid_streaming)}")
    print(f"Valid both: {np.sum(valid_both)}")
    
    if np.sum(valid_both) > 0:
        max_diff = np.max(np.abs(bulk_result[valid_both] - streaming_array[valid_both]))
        print(f"Max difference: {max_diff:.2e}")
        print(f"Accuracy: {np.mean(np.abs(bulk_result[valid_both] - streaming_array[valid_both]) < 1e-10) * 100:.1f}%")
    
    # === Test 6: Profile the streaming function ===
    print(f"\n⚡ PROFILING STREAMING FUNCTION:")
    
    import cProfile
    import pstats
    import io
    
    def profile_streaming():
        sma_stream = SMAStreaming(20)
        for price in close:
            sma_stream.update(price)
    
    pr = cProfile.Profile()
    pr.enable()
    profile_streaming()
    pr.disable()
    
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(10)
    
    print(s.getvalue())

if __name__ == "__main__":
    investigate_benchmark_discrepancy()
    
    print("\n🎯 ANALYSIS:")
    print("=" * 50)
    print("The streaming implementation IS using the optimized sliding window approach.")
    print("The performance difference might be due to:")
    print("1. JIT compilation overhead not properly warmed up")
    print("2. Function call overhead in the streaming loop")
    print("3. Python object creation overhead")
    print("4. Memory allocation patterns")
    print("5. Different data generation causing different cache behavior")