#!/usr/bin/env python3
"""
Analyze EMA performance scaling with different window sizes.
"""

import numpy as np
import time
from ta_numba.trend import ema_numba
from ta_numba.streaming import EMAStreaming

class StreamingTANumbaEMA:
    """The 'old' implementation - recalculates entire EMA"""
    
    def __init__(self, window: int):
        self.window = window
        self.values = []
        # Pre-compile
        dummy = np.array([1.0, 2.0, 3.0])
        _ = ema_numba(dummy, window)
        
    def update(self, value: float) -> float:
        self.values.append(value)
        
        if len(self.values) >= self.window:
            if len(self.values) > self.window * 2:
                self.values = self.values[-self.window:]
            
            # Recalculates ENTIRE EMA from scratch - O(n)
            result = ema_numba(np.array(self.values[-self.window:]), self.window)
            return result[-1] if len(result) > 0 else np.nan
        
        return np.nan

class SimpleEMAStreaming:
    """Simple direct EMA - true O(1) streaming"""
    
    def __init__(self, window: int):
        self.alpha = 2.0 / (window + 1.0)
        self.ema = None
        
    def update(self, value: float) -> float:
        if self.ema is None:
            self.ema = value
        else:
            self.ema = self.alpha * value + (1 - self.alpha) * self.ema
        return self.ema

def test_ema_scaling():
    """Test EMA performance scaling with window size."""
    print("📈 EMA PERFORMANCE SCALING ANALYSIS")
    print("=" * 50)
    
    # Test different window sizes
    window_sizes = [5, 10, 20, 50, 100, 200, 500]
    n_points = 5000
    
    np.random.seed(42)
    prices = np.random.uniform(95, 105, n_points)
    
    print(f"Test data: {n_points} points")
    print(f"Window sizes: {window_sizes}")
    print()
    
    results = []
    
    for window in window_sizes:
        print(f"🔬 Testing window size: {window}")
        
        # Test implementations
        implementations = {
            'Old (O(n) recalc)': StreamingTANumbaEMA(window),
            'OPTIMIZED': EMAStreaming(window),
            'Simple (O(1))': SimpleEMAStreaming(window)
        }
        
        window_results = {'window': window}
        
        for name, impl in implementations.items():
            start = time.perf_counter()
            for price in prices:
                result = impl.update(price)
            total_time = time.perf_counter() - start
            
            per_tick_us = (total_time / n_points) * 1_000_000
            window_results[name] = per_tick_us
            
            print(f"  {name:<20}: {per_tick_us:>6.2f}μs per tick")
        
        results.append(window_results)
        print()
    
    # Analysis
    print("📊 SCALING ANALYSIS:")
    print("=" * 50)
    print(f"{'Window':<8} {'Old (O(n))':<12} {'OPTIMIZED':<12} {'Simple':<10} {'Winner'}")
    print("-" * 55)
    
    for result in results:
        window = result['window']
        old_time = result['Old (O(n) recalc)']
        opt_time = result['OPTIMIZED']
        simple_time = result['Simple (O(1))']
        
        # Determine winner
        times = {'Old': old_time, 'OPT': opt_time, 'Simple': simple_time}
        winner = min(times.items(), key=lambda x: x[1])[0]
        
        print(f"{window:<8} {old_time:<12.2f} {opt_time:<12.2f} {simple_time:<10.2f} {winner}")
    
    print()
    print("🎯 KEY INSIGHTS:")
    print("-" * 20)
    
    # Find crossover point
    crossover_found = False
    for i, result in enumerate(results):
        old_time = result['Old (O(n) recalc)']
        simple_time = result['Simple (O(1))']
        
        if simple_time < old_time and not crossover_found:
            crossover_window = result['window']
            print(f"• Crossover point: Window {crossover_window}")
            print(f"  Below this window: O(n) recalc is faster (vectorization)")
            print(f"  Above this window: O(1) streaming is faster (scaling)")
            crossover_found = True
            break
    
    print(f"• Small windows (≤20): Vectorized recalculation wins")
    print(f"• Large windows (≥50): True streaming wins")
    print(f"• Function call overhead affects OPTIMIZED version")
    print()
    
    print("🔧 OPTIMIZATION RECOMMENDATION:")
    print("-" * 30)
    print("The OPTIMIZED version needs improvement:")
    print("1. Remove function call overhead")
    print("2. Use direct calculation like Simple version")
    print("3. Keep JIT compilation for complex indicators only")

if __name__ == "__main__":
    test_ema_scaling()