#!/usr/bin/env python3
"""
Audit all streaming indicators for performance optimization opportunities.
"""

import numpy as np
import time
from typing import Dict, List

# Import all streaming indicators
from ta_numba.streaming import (
    SMAStreaming, EMAStreaming, WMAStreaming, MACDStreaming, ADXStreaming,
    VortexIndicatorStreaming, TRIXStreaming, CCIStreaming, DPOStreaming,
    AroonStreaming, ParabolicSARStreaming,
    RSIStreaming, StochasticStreaming, WilliamsRStreaming, ROCStreaming,
    UltimateOscillatorStreaming, StochasticRSIStreaming, TSIStreaming,
    AwesomeOscillatorStreaming, KAMAStreaming, PPOStreaming, MomentumStreaming,
    ATRStreaming, BBandsStreaming, KeltnerChannelStreaming, DonchianChannelStreaming,
    StandardDeviationStreaming, VarianceStreaming, RangeStreaming,
    HistoricalVolatilityStreaming, UlcerIndexStreaming,
    MoneyFlowIndexStreaming, AccDistIndexStreaming, OnBalanceVolumeStreaming,
    ChaikinMoneyFlowStreaming, ForceIndexStreaming, EaseOfMovementStreaming,
    VolumePriceTrendStreaming, NegativeVolumeIndexStreaming, VWAPStreaming,
    VWEMAStreaming,
    DailyReturnStreaming, DailyLogReturnStreaming, CumulativeReturnStreaming,
    CompoundLogReturnStreaming, RollingReturnStreaming, VolatilityStreaming,
    SharpeRatioStreaming, MaxDrawdownStreaming, CalmarRatioStreaming
)

def create_test_data(n_points: int = 1000):
    """Create test OHLCV data."""
    np.random.seed(42)
    
    # Generate realistic price series
    base_price = 100.0
    prices = [base_price]
    for i in range(1, n_points):
        change = np.random.normal(0.0001, 0.02)
        new_price = prices[-1] * (1 + change)
        prices.append(max(new_price, 0.01))
    
    close = np.array(prices)
    high = close * np.random.uniform(1.000, 1.020, n_points)
    low = close * np.random.uniform(0.980, 1.000, n_points)
    open_price = close * np.random.uniform(0.995, 1.005, n_points)
    volume = np.random.randint(1000, 10000, n_points)
    
    return {
        'open': open_price,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume.astype(float)
    }

def benchmark_indicator(indicator_class, data: Dict, *args, **kwargs) -> Dict:
    """Benchmark a single indicator."""
    try:
        # Determine input requirements
        indicator = indicator_class(*args, **kwargs)
        
        # Get method signature
        import inspect
        update_sig = inspect.signature(indicator.update)
        param_count = len(update_sig.parameters)
        
        n_points = len(data['close'])
        
        # Time the indicator
        start = time.perf_counter()
        
        if param_count == 1:
            # Single input (close)
            for value in data['close']:
                result = indicator.update(value)
        elif param_count == 2:
            # Two inputs (close, volume)
            for close, volume in zip(data['close'], data['volume']):
                result = indicator.update(close, volume)
        elif param_count == 3:
            # Three inputs (high, low, close)
            for high, low, close in zip(data['high'], data['low'], data['close']):
                result = indicator.update(high, low, close)
        elif param_count == 4:
            # Four inputs (high, low, close, volume)
            for high, low, close, volume in zip(data['high'], data['low'], data['close'], data['volume']):
                result = indicator.update(high, low, close, volume)
        else:
            return {'error': f"Unsupported parameter count: {param_count}"}
        
        total_time = time.perf_counter() - start
        per_tick_us = (total_time / n_points) * 1_000_000
        
        return {
            'total_time': total_time,
            'per_tick_us': per_tick_us,
            'final_result': result,
            'param_count': param_count,
            'success': True
        }
        
    except Exception as e:
        return {'error': str(e), 'success': False}

def audit_all_indicators():
    """Audit all streaming indicators for performance."""
    print("🔍 COMPREHENSIVE STREAMING INDICATOR AUDIT")
    print("=" * 60)
    
    # Generate test data
    data = create_test_data(5000)
    print(f"Test data: {len(data['close'])} points")
    print()
    
    # Define indicators to test with their default parameters
    indicators_to_test = [
        # Trend indicators
        (SMAStreaming, [20], {}),
        (EMAStreaming, [20], {}),
        (WMAStreaming, [20], {}),
        (MACDStreaming, [12, 26, 9], {}),
        
        # Momentum indicators  
        (RSIStreaming, [14], {}),
        (ROCStreaming, [10], {}),
        (MomentumStreaming, [10], {}),
        
        # Volatility indicators
        (ATRStreaming, [14], {}),
        (BBandsStreaming, [20, 2.0], {}),
        (StandardDeviationStreaming, [20], {}),
        (VarianceStreaming, [20], {}),
        
        # Volume indicators
        (OnBalanceVolumeStreaming, [], {}),
        (MoneyFlowIndexStreaming, [14], {}),
        (VWAPStreaming, [], {}),
        
        # Others
        (DailyReturnStreaming, [], {}),
        (VolatilityStreaming, [20], {}),
        (RollingReturnStreaming, [20], {}),
    ]
    
    results = []
    
    print("📊 PERFORMANCE RESULTS:")
    print("-" * 40)
    print(f"{'Indicator':<25} {'Time (μs)':<12} {'Status':<10} {'Notes'}")
    print("-" * 60)
    
    for indicator_class, args, kwargs in indicators_to_test:
        name = indicator_class.__name__.replace('Streaming', '')
        
        result = benchmark_indicator(indicator_class, data, *args, **kwargs)
        
        if result['success']:
            per_tick = result['per_tick_us']
            status = "✅ FAST" if per_tick < 1.0 else "⚠️ SLOW" if per_tick < 5.0 else "❌ VERY SLOW"
            notes = f"{result['param_count']} params"
            
            print(f"{name:<25} {per_tick:<12.2f} {status:<10} {notes}")
            
            results.append({
                'name': name,
                'class': indicator_class,
                'per_tick_us': per_tick,
                'args': args,
                'kwargs': kwargs
            })
        else:
            print(f"{name:<25} {'ERROR':<12} {'❌ FAILED':<10} {result['error'][:20]}...")
    
    print()
    
    # Analysis
    print("🎯 PERFORMANCE ANALYSIS:")
    print("-" * 25)
    
    fast_indicators = [r for r in results if r['per_tick_us'] < 1.0]
    slow_indicators = [r for r in results if r['per_tick_us'] >= 1.0]
    
    print(f"Fast indicators (< 1μs): {len(fast_indicators)}")
    print(f"Slow indicators (≥ 1μs): {len(slow_indicators)}")
    
    if slow_indicators:
        print(f"\n🔧 INDICATORS NEEDING OPTIMIZATION:")
        slow_indicators.sort(key=lambda x: x['per_tick_us'], reverse=True)
        for indicator in slow_indicators:
            print(f"  {indicator['name']}: {indicator['per_tick_us']:.2f}μs")
    
    # Identify optimization opportunities
    print(f"\n💡 OPTIMIZATION OPPORTUNITIES:")
    print("-" * 30)
    
    # Check for function call overhead patterns
    overhead_patterns = []
    
    # Read source files to identify patterns
    import os
    streaming_dir = "../src/ta_numba/streaming"
    if os.path.exists(streaming_dir):
        for filename in ['trend.py', 'momentum.py', 'volatility.py', 'volume.py', 'others.py']:
            filepath = os.path.join(streaming_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    content = f.read()
                    if '_streaming_' in content:
                        overhead_patterns.append(filename)
    
    if overhead_patterns:
        print("Files with potential JIT function call overhead:")
        for pattern in overhead_patterns:
            print(f"  {pattern}")
    
    print("\nRecommendations:")
    print("1. Replace JIT function calls with direct calculations for simple operations")
    print("2. Keep JIT functions only for complex mathematical operations")
    print("3. Use direct calculation for: EMA, SMA, basic arithmetic")
    print("4. Keep JIT for: complex indicators with multiple calculations")
    
    return results

if __name__ == "__main__":
    results = audit_all_indicators()