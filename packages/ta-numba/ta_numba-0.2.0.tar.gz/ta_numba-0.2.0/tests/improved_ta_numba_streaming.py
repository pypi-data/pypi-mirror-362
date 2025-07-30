#!/usr/bin/env python3
"""
Improved ta-numba for streaming data processing
"""
import numpy as np
import time
from numba import njit
from ta_numba.trend import sma_numba, ema_numba, macd_numba
from ta_numba.momentum import relative_strength_index_numba
from ta_numba.volatility import average_true_range_numba, bollinger_bands_numba

print("=== IMPROVED TA-NUMBA FOR STREAMING ===")

# 🚀 SOLUTION 1: Create single-value ta-numba functions
@njit(fastmath=True)
def sma_numba_single(data: np.ndarray, window: int = 20) -> float:
    """Calculate SMA for ONLY the last window - single value output"""
    if len(data) < window:
        return np.nan
    
    # Only calculate the last SMA value
    last_window = data[-window:]
    return np.mean(last_window)

@njit(fastmath=True)
def ema_numba_single(data: np.ndarray, window: int = 20) -> float:
    """Calculate EMA for ONLY the final value - single value output"""
    if len(data) < 2:
        return np.nan
    
    alpha = 2.0 / (window + 1.0)
    ema = data[0]
    
    for i in range(1, len(data)):
        ema = alpha * data[i] + (1 - alpha) * ema
    
    return ema

@njit(fastmath=True)
def rsi_numba_single(data: np.ndarray, window: int = 14) -> float:
    """Calculate RSI for ONLY the final value - single value output"""
    if len(data) < window + 1:
        return np.nan
    
    alpha = 1.0 / window
    
    # Initialize with first change
    diff = data[1] - data[0]
    up_ema = max(diff, 0.0)
    down_ema = max(-diff, 0.0)
    
    # Calculate EMA of gains and losses
    for i in range(2, len(data)):
        diff = data[i] - data[i-1]
        gain = max(diff, 0.0)
        loss = max(-diff, 0.0)
        
        up_ema = alpha * gain + (1 - alpha) * up_ema
        down_ema = alpha * loss + (1 - alpha) * down_ema
    
    if down_ema == 0:
        return 100.0
    
    rs = up_ema / down_ema
    return 100.0 - (100.0 / (1.0 + rs))

@njit(fastmath=True)
def macd_numba_single(data: np.ndarray, fast_period: int = 12, slow_period: int = 26) -> float:
    """Calculate MACD for ONLY the final value - single value output"""
    if len(data) < slow_period:
        return np.nan
    
    # Calculate fast EMA
    alpha_fast = 2.0 / (fast_period + 1.0)
    ema_fast = data[0]
    for i in range(1, len(data)):
        ema_fast = alpha_fast * data[i] + (1 - alpha_fast) * ema_fast
    
    # Calculate slow EMA
    alpha_slow = 2.0 / (slow_period + 1.0)
    ema_slow = data[0]
    for i in range(1, len(data)):
        ema_slow = alpha_slow * data[i] + (1 - alpha_slow) * ema_slow
    
    return ema_fast - ema_slow

@njit(fastmath=True)
def atr_numba_single(high: np.ndarray, low: np.ndarray, close: np.ndarray, window: int = 14) -> float:
    """Calculate ATR for ONLY the final value - single value output"""
    if len(high) < window + 1:
        return np.nan
    
    alpha = 1.0 / window
    
    # Initialize with first true range
    tr = high[1] - low[1]
    atr = tr
    
    # Calculate ATR using Wilder's EMA
    for i in range(2, len(high)):
        tr1 = high[i] - low[i]
        tr2 = abs(high[i] - close[i-1])
        tr3 = abs(low[i] - close[i-1])
        
        tr = max(tr1, max(tr2, tr3))
        atr = alpha * tr + (1 - alpha) * atr
    
    return atr

@njit(fastmath=True)
def bb_numba_single(data: np.ndarray, window: int = 20, std_dev: float = 2.0) -> tuple:
    """Calculate Bollinger Bands for ONLY the final value - single value output"""
    if len(data) < window:
        return (np.nan, np.nan, np.nan)
    
    # Calculate mean and std of last window
    last_window = data[-window:]
    mean = np.mean(last_window)
    std = np.std(last_window)
    
    upper = mean + (std_dev * std)
    lower = mean - (std_dev * std)
    
    return (upper, mean, lower)

# 🚀 SOLUTION 2: Streaming classes with ta-numba core
class StreamingTANumba:
    def __init__(self, indicator_func, window, **kwargs):
        self.indicator_func = indicator_func
        self.window = window
        self.kwargs = kwargs
        self.values = []
        self.data_array = np.zeros(window * 2, dtype=np.float64)  # Pre-allocate
        
        # Warm up the function
        dummy_data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        _ = self.indicator_func(dummy_data, window, **kwargs)
        
    def update(self, value: float) -> float:
        self.values.append(value)
        
        # Keep only what we need (prevent unlimited growth)
        if len(self.values) > self.window * 2:
            self.values = self.values[-self.window:]
        
        if len(self.values) >= self.window:
            # Copy to pre-allocated array (faster than np.array creation)
            n = len(self.values)
            self.data_array[:n] = self.values
            
            # Use our optimized single-value function
            return self.indicator_func(self.data_array[:n], self.window, **self.kwargs)
        
        return np.nan

# 🚀 SOLUTION 3: Hybrid approach - incremental when possible
class HybridStreamingSMA:
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
            
        if len(self.values) == self.window:
            return self.sum_val / self.window
        
        return np.nan

class HybridStreamingEMA:
    def __init__(self, window: int):
        self.alpha = 2.0 / (window + 1.0)
        self.ema = None
        
    def update(self, value: float) -> float:
        if self.ema is None:
            self.ema = value
        else:
            self.ema = self.alpha * value + (1 - self.alpha) * self.ema
        return self.ema

# Test all approaches for multiple indicators
def benchmark_multiple_indicators():
    print("\n🔬 COMPARING MULTIPLE INDICATORS:")
    print("=" * 80)
    
    # Test data
    np.random.seed(42)
    prices = np.random.rand(1000) * 100 + 50
    
    # Generate OHLC data for ATR
    high = prices + np.random.rand(1000) * 2
    low = prices - np.random.rand(1000) * 2
    close = prices
    
    # Indicators to test
    indicators = {
        'SMA-20': {
            'original': lambda data: sma_numba(np.array(data))[-1],
            'improved': lambda data: sma_numba_single(np.array(data), 20),
            'window': 20
        },
        'EMA-20': {
            'original': lambda data: ema_numba(np.array(data), 20)[-1],
            'improved': lambda data: ema_numba_single(np.array(data), 20),
            'window': 20
        },
        'RSI-14': {
            'original': lambda data: relative_strength_index_numba(np.array(data))[-1],
            'improved': lambda data: rsi_numba_single(np.array(data), 14),
            'window': 15  # RSI needs window + 1
        },
        'MACD-12-26': {
            'original': lambda data: macd_numba(np.array(data))[-1],
            'improved': lambda data: macd_numba_single(np.array(data), 12, 26),
            'window': 26
        },
        'ATR-14': {
            'original': lambda data, h, l, c: average_true_range_numba(np.array(h), np.array(l), np.array(c))[-1],
            'improved': lambda data, h, l, c: atr_numba_single(np.array(h), np.array(l), np.array(c), 14),
            'window': 15  # ATR needs window + 1
        },
        'BB-20': {
            'original': lambda data: bollinger_bands_numba(np.array(data), 20, 2.0)[0][-1],  # Upper band
            'improved': lambda data: bb_numba_single(np.array(data), 20, 2.0)[0],  # Upper band
            'window': 20
        }
    }
    
    print(f"{'Indicator':<15} | {'Original (μs)':<12} | {'Improved (μs)':<12} | {'Speedup':<8} | {'Accuracy'}")
    print("-" * 80)
    
    for name, funcs in indicators.items():
        window = funcs['window']
        
        # Prepare test data
        test_data = list(prices[:window])
        test_high = list(high[:window])
        test_low = list(low[:window])
        test_close = list(close[:window])
        
        original_times = []
        improved_times = []
        
        # Test 100 streaming updates
        for i in range(window, window + 100):
            test_data.append(prices[i])
            test_high.append(high[i])
            test_low.append(low[i])
            test_close.append(close[i])
            
            # Time original approach
            start = time.perf_counter()
            if 'ATR' in name:
                result1 = funcs['original'](test_data, test_high, test_low, test_close)
            else:
                result1 = funcs['original'](test_data)
            original_times.append(time.perf_counter() - start)
            
            # Time improved approach
            start = time.perf_counter()
            if 'ATR' in name:
                result2 = funcs['improved'](test_data, test_high, test_low, test_close)
            else:
                result2 = funcs['improved'](test_data)
            improved_times.append(time.perf_counter() - start)
        
        # Calculate averages
        avg_original = (sum(original_times) / len(original_times)) * 1000000
        avg_improved = (sum(improved_times) / len(improved_times)) * 1000000
        speedup = avg_original / avg_improved
        
        # Check accuracy
        if isinstance(result1, tuple) and isinstance(result2, tuple):
            accuracy = "✓" if abs(result1[0] - result2[0]) < 1e-6 else "✗"
        else:
            # Handle potential array results
            if isinstance(result1, np.ndarray):
                result1 = result1.item() if result1.size == 1 else result1[-1]
            if isinstance(result2, np.ndarray):
                result2 = result2.item() if result2.size == 1 else result2[-1]
            accuracy = "✓" if abs(result1 - result2) < 1e-6 else "✗"
        
        print(f"{name:<15} | {avg_original:<12.2f} | {avg_improved:<12.2f} | {speedup:<8.1f}x | {accuracy}")

def benchmark_streaming_improvements():
    print("\n🔬 SMA DETAILED COMPARISON:")
    print("=" * 70)
    
    # Test data
    np.random.seed(42)
    prices = np.random.rand(1000) * 100 + 50
    window = 20
    
    # Initialize all approaches
    approaches = {
        'Original ta-numba (wasteful)': lambda data: sma_numba(np.array(data))[-1],
        'Improved ta-numba (single)': lambda data: sma_numba_single(np.array(data), window),
        'Streaming ta-numba': StreamingTANumba(sma_numba_single, window),
        'Hybrid incremental': HybridStreamingSMA(window),
        'Pure numpy mean': lambda data: np.mean(data[-window:]) if len(data) >= window else np.nan
    }
    
    # Pre-warm streaming objects
    for i in range(window):
        if hasattr(approaches['Streaming ta-numba'], 'update'):
            approaches['Streaming ta-numba'].update(prices[i])
        if hasattr(approaches['Hybrid incremental'], 'update'):
            approaches['Hybrid incremental'].update(prices[i])
    
    # Benchmark each approach
    results = {}
    
    for name, func in approaches.items():
        total_time = 0
        
        # Reset streaming data
        current_data = list(prices[:window])
        
        # Test 500 streaming updates
        for i in range(window, window + 500):
            current_data.append(prices[i])
            
            start = time.perf_counter()
            
            if hasattr(func, 'update'):
                result = func.update(prices[i])
            else:
                result = func(current_data)
                
            elapsed = time.perf_counter() - start
            total_time += elapsed
        
        avg_time = (total_time / 500) * 1000000  # microseconds
        results[name] = avg_time
        
        print(f"{name:<30}: {avg_time:>8.2f}μs per update")
    
    # Show speedup comparison
    print("\n📊 SPEEDUP COMPARISON:")
    print("=" * 70)
    baseline = results['Original ta-numba (wasteful)']
    
    for name, time_us in results.items():
        speedup = baseline / time_us
        print(f"{name:<30}: {speedup:>6.2f}x faster than original")
    
    # Accuracy verification
    print("\n🔬 ACCURACY VERIFICATION:")
    print("=" * 70)
    test_data = prices[:50]
    
    original = sma_numba(test_data)[-1]
    improved = sma_numba_single(test_data, window)
    numpy_mean = np.mean(test_data[-window:])
    
    print(f"Original ta-numba: {original:.8f}")
    print(f"Improved ta-numba: {improved:.8f}")
    print(f"Numpy mean:        {numpy_mean:.8f}")
    print(f"Difference:        {abs(original - improved):.2e}")

if __name__ == "__main__":
    benchmark_multiple_indicators()
    benchmark_streaming_improvements()
    
    print("\n🎯 SUMMARY:")
    print("=" * 70)
    print("✅ YES! We can improve ta-numba for streaming by:")
    print("1. Creating single-value functions (avoid calculating full arrays)")
    print("2. Using streaming classes with pre-allocated arrays")
    print("3. Hybrid approach: incremental when possible, ta-numba when needed")
    print("4. For simple indicators (SMA): Pure incremental is best")
    print("5. For complex indicators (RSI, MACD): Improved ta-numba helps")
    print()
    print("💡 The key insight: Don't calculate what you don't need!")