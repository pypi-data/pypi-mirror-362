#!/usr/bin/env python3
"""
Debug why the "old" streaming EMA is faster than the "optimized" version.
"""

import numpy as np
import time
from ta_numba.trend import ema_numba
from ta_numba.streaming import EMAStreaming

class StreamingTANumbaEMA:
    """The 'old' implementation from test_nautilus_real_speed.py"""
    
    def __init__(self, window: int):
        self.window = window
        self.values = []
        # Pre-compile the function with warm-up
        dummy = np.array([1.0, 2.0, 3.0])
        _ = ema_numba(dummy, window)  # Ensure JIT compilation
        
    def update(self, value: float) -> float:
        self.values.append(value)
        
        if len(self.values) >= self.window:
            if len(self.values) > self.window * 2:  # Prevent unbounded growth
                self.values = self.values[-self.window:]
            
            # Use actual ta-numba function on current window
            result = ema_numba(np.array(self.values[-self.window:]), self.window)
            return result[-1] if len(result) > 0 else np.nan
        
        return np.nan

class SimpleEMAStreaming:
    """Simple direct EMA calculation"""
    
    def __init__(self, window: int):
        self.alpha = 2.0 / (window + 1.0)
        self.ema = None
        
    def update(self, value: float) -> float:
        if self.ema is None:
            self.ema = value
        else:
            self.ema = self.alpha * value + (1 - self.alpha) * self.ema
        return self.ema

def debug_ema_performance():
    """Debug the EMA performance difference."""
    print("🔍 DEBUGGING EMA PERFORMANCE DIFFERENCE")
    print("=" * 50)
    
    # Generate test data
    np.random.seed(42)
    n_points = 10000
    prices = np.random.uniform(95, 105, n_points)
    window = 20
    
    print(f"Test data: {n_points} points")
    print(f"Window: {window}")
    print()
    
    # Implementations to test
    implementations = {
        'Old ta-numba Streaming': StreamingTANumbaEMA(window),
        'OPTIMIZED EMAStreaming': EMAStreaming(window),
        'Simple Direct EMA': SimpleEMAStreaming(window)
    }
    
    results = {}
    
    for name, impl in implementations.items():
        print(f"Testing {name}...")
        
        # Time the implementation
        start = time.perf_counter()
        for price in prices:
            result = impl.update(price)
        total_time = time.perf_counter() - start
        
        per_tick_us = (total_time / n_points) * 1_000_000
        results[name] = (total_time, per_tick_us, result)
        
        print(f"  Total time: {total_time:.4f}s")
        print(f"  Per tick: {per_tick_us:.2f}μs")
        print(f"  Final value: {result:.6f}")
        print()
    
    # Analysis
    print("📊 PERFORMANCE ANALYSIS:")
    print("-" * 30)
    
    sorted_results = sorted(results.items(), key=lambda x: x[1][1])
    fastest_time = sorted_results[0][1][1]
    
    for name, (total_time, per_tick_us, final_val) in sorted_results:
        speedup = fastest_time / per_tick_us if per_tick_us > 0 else 0
        print(f"{name:<25}: {per_tick_us:>6.2f}μs ({speedup:>4.1f}x faster than slowest)")
    
    print()
    print("🔍 ROOT CAUSE ANALYSIS:")
    print("-" * 30)
    
    print("1. 'Old ta-numba Streaming' approach:")
    print("   - Calls ema_numba() function every update")
    print("   - But ema_numba() recalculates the ENTIRE EMA from scratch")
    print("   - This is actually NOT optimized for streaming!")
    print()
    
    print("2. 'OPTIMIZED EMAStreaming' approach:")
    print("   - Uses proper incremental EMA calculation")
    print("   - Calls JIT-compiled _streaming_ema_update()")
    print("   - True O(1) update per tick")
    print()
    
    print("3. 'Simple Direct EMA' approach:")
    print("   - Pure Python EMA calculation")
    print("   - No function call overhead")
    print("   - Direct mathematical operation")
    print()
    
    # Let's investigate the function call overhead
    print("🔬 INVESTIGATING FUNCTION CALL OVERHEAD:")
    print("-" * 40)
    
    # Test just the function calls
    from ta_numba.streaming.base import _streaming_ema_update
    
    # Warm up
    _ = _streaming_ema_update(100.0, 101.0, 0.095)
    
    # Test function call overhead
    start = time.perf_counter()
    prev_ema = 100.0
    alpha = 2.0 / 21.0
    for price in prices[:1000]:
        prev_ema = _streaming_ema_update(prev_ema, price, alpha)
    jit_time = time.perf_counter() - start
    
    # Test direct calculation
    start = time.perf_counter()
    ema = 100.0
    alpha = 2.0 / 21.0
    for price in prices[:1000]:
        ema = alpha * price + (1 - alpha) * ema
    direct_time = time.perf_counter() - start
    
    print(f"JIT function calls (1000 updates): {jit_time*1000:.3f}ms")
    print(f"Direct calculation (1000 updates): {direct_time*1000:.3f}ms")
    print(f"Function call overhead: {(jit_time/direct_time):,.1f}x slower")
    
    print()
    print("🎯 CONCLUSION:")
    print("-" * 15)
    print("The 'old' implementation is misleadingly labeled!")
    print("It's actually calling ema_numba() which recalculates the entire EMA.")
    print("For large windows, this becomes inefficient.")
    print("The OPTIMIZED version uses true O(1) incremental updates.")
    print()
    print("However, for small windows (like 20), the bulk recalculation")
    print("might be faster due to vectorization, despite being O(n).")

if __name__ == "__main__":
    debug_ema_performance()