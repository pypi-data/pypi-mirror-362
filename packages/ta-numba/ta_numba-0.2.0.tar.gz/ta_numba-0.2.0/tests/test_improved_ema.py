#!/usr/bin/env python3
"""
Test the improved EMA implementation.
"""

import numpy as np
import time
from ta_numba.streaming import EMAStreaming

class SimpleEMAStreaming:
    """Simple direct EMA"""
    
    def __init__(self, window: int):
        self.alpha = 2.0 / (window + 1.0)
        self.ema = None
        
    def update(self, value: float) -> float:
        if self.ema is None:
            self.ema = value
        else:
            self.ema = self.alpha * value + (1 - self.alpha) * self.ema
        return self.ema

def test_improved_ema():
    """Test the improved EMA implementation."""
    print("🚀 TESTING IMPROVED EMA IMPLEMENTATION")
    print("=" * 45)
    
    # Generate test data
    np.random.seed(42)
    n_points = 10000
    prices = np.random.uniform(95, 105, n_points)
    window = 20
    
    print(f"Test data: {n_points} points")
    print(f"Window: {window}")
    print()
    
    # Test implementations
    implementations = {
        'Improved EMAStreaming': EMAStreaming(window),
        'Simple Direct EMA': SimpleEMAStreaming(window)
    }
    
    results = {}
    
    for name, impl in implementations.items():
        print(f"Testing {name}...")
        
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
    
    # Compare results
    print("📊 PERFORMANCE COMPARISON:")
    print("-" * 30)
    
    sorted_results = sorted(results.items(), key=lambda x: x[1][1])
    
    for name, (total_time, per_tick_us, final_val) in sorted_results:
        print(f"{name:<25}: {per_tick_us:>6.2f}μs per tick")
    
    # Check accuracy
    ema_result = results['Improved EMAStreaming'][2]
    simple_result = results['Simple Direct EMA'][2]
    
    print()
    print("🎯 ACCURACY CHECK:")
    print("-" * 18)
    print(f"Improved EMAStreaming: {ema_result:.10f}")
    print(f"Simple Direct EMA:     {simple_result:.10f}")
    print(f"Difference:            {abs(ema_result - simple_result):.2e}")
    print("✅ Results match!" if abs(ema_result - simple_result) < 1e-10 else "❌ Results differ!")

if __name__ == "__main__":
    test_improved_ema()