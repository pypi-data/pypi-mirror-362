#!/usr/bin/env python3
"""
Properly optimized ta-numba streaming implementation
"""
import numpy as np
import time
from numba import njit

@njit(fastmath=True)
def single_sma_numba(data: np.ndarray) -> float:
    """Calculate SMA for just the final window - single value output"""
    return np.mean(data)

@njit(fastmath=True) 
def single_ema_numba(data: np.ndarray, alpha: float) -> float:
    """Calculate EMA incrementally - single value output"""
    result = data[0]
    for i in range(1, len(data)):
        result = alpha * data[i] + (1 - alpha) * result
    return result

# Optimal ta-numba streaming implementations
class OptimalTANumbaSMA:
    def __init__(self, window: int):
        self.window = window
        self.values = []
        # Pre-allocate array
        self.data_array = np.zeros(window, dtype=np.float64)
        # Warm up
        _ = single_sma_numba(self.data_array)
        
    def update(self, value: float) -> float:
        self.values.append(value)
        
        if len(self.values) >= self.window:
            if len(self.values) > self.window * 2:
                self.values = self.values[-self.window:]
            
            # Copy to pre-allocated array
            for i, val in enumerate(self.values[-self.window:]):
                self.data_array[i] = val
                
            # Single optimized calculation
            return single_sma_numba(self.data_array)
        
        return np.nan

class OptimalTANumbaEMA:
    def __init__(self, window: int):
        self.window = window
        self.alpha = 2.0 / (window + 1.0)
        self.values = []
        self.data_array = np.zeros(window, dtype=np.float64)
        # Warm up
        _ = single_ema_numba(self.data_array, self.alpha)
        
    def update(self, value: float) -> float:
        self.values.append(value)
        
        if len(self.values) >= self.window:
            if len(self.values) > self.window * 2:
                self.values = self.values[-self.window:]
            
            # Copy to pre-allocated array
            for i, val in enumerate(self.values[-self.window:]):
                self.data_array[i] = val
                
            # Single optimized calculation  
            return single_ema_numba(self.data_array, self.alpha)
        
        return np.nan

# Alternative: Pure incremental approach (should be fastest)
class TrueStreamingSMA:
    def __init__(self, window: int):
        self.window = window
        self.values = []
        self.sum_val = 0.0
        
    def update(self, value: float) -> float:
        self.values.append(value)
        self.sum_val += value
        
        if len(self.values) > self.window:
            old_val = self.values.pop(0)
            self.sum_val -= old_val
            
        return self.sum_val / len(self.values) if len(self.values) == self.window else np.nan

class TrueStreamingEMA:
    def __init__(self, window: int):
        self.alpha = 2.0 / (window + 1.0)
        self.ema = None
        
    def update(self, value: float) -> float:
        if self.ema is None:
            self.ema = value
        else:
            self.ema = self.alpha * value + (1 - self.alpha) * self.ema
        return self.ema

print("=== OPTIMIZED TA-NUMBA STREAMING COMPARISON ===")

# Test data
np.random.seed(42)
prices = np.random.rand(1000) * 100 + 50
window = 20

# Initialize all implementations
optimal_sma = OptimalTANumbaSMA(window)
optimal_ema = OptimalTANumbaEMA(window)
true_sma = TrueStreamingSMA(window)
true_ema = TrueStreamingEMA(window)

# Pre-fill
for i in range(window):
    optimal_sma.update(prices[i])
    optimal_ema.update(prices[i])
    true_sma.update(prices[i])
    true_ema.update(prices[i])

print("\n🔬 STREAMING PERFORMANCE COMPARISON:")
print("=" * 50)

def benchmark_streaming(name, sma_obj, iterations=1000):
    test_value = 75.0
    start = time.perf_counter()
    for _ in range(iterations):
        result = sma_obj.update(test_value)
    elapsed = time.perf_counter() - start
    avg_time = (elapsed / iterations) * 1000000
    print(f"{name:<30}: {avg_time:>8.2f}μs per update")
    return avg_time

benchmark_streaming("Optimal ta-numba SMA", optimal_sma)
benchmark_streaming("True Streaming SMA", true_sma)
benchmark_streaming("Optimal ta-numba EMA", optimal_ema)
benchmark_streaming("True Streaming EMA", true_ema)

print("\n🔬 VERIFICATION - RESULTS SHOULD BE IDENTICAL:")
print("=" * 50)

test_prices = [50, 51, 52, 53, 54, 55, 56, 57, 58, 59]

# Reset
opt_sma = OptimalTANumbaSMA(5)
true_sma = TrueStreamingSMA(5)

print("Price | Optimal ta-numba | True Streaming | Difference")
print("-" * 55)

for price in test_prices:
    opt_result = opt_sma.update(price)
    true_result = true_sma.update(price)
    diff = abs(opt_result - true_result) if not np.isnan(opt_result) and not np.isnan(true_result) else 0
    print(f"{price:5.1f} | {opt_result:15.6f} | {true_result:14.6f} | {diff:10.8f}")

print("\n📊 CONCLUSION:")
print("=" * 50)
print("If optimized ta-numba streaming is still slower than pure Python:")
print("1. ✅ JIT overhead for small arrays dominates")
print("2. ✅ Function call overhead is significant")  
print("3. ✅ Incremental algorithms are fundamentally superior for streaming")
print("4. ✅ ta-numba is best for bulk processing, not real-time updates")
print()
print("For real-time trading:")
print("🚀 Use pure incremental algorithms (True Streaming)")
print("📊 Use ta-numba for historical analysis and backtesting")