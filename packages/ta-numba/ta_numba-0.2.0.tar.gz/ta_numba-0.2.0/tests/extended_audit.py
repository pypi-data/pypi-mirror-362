#!/usr/bin/env python3
"""
Extended audit of all 53 streaming indicators.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import time
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

# Import all streaming indicators
try:
    from ta_numba.streaming import *
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

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

def test_indicator(indicator_class, data: Dict, *args, **kwargs):
    """Test a single indicator with error handling."""
    try:
        # Create indicator
        indicator = indicator_class(*args, **kwargs)
        
        # Determine input requirements
        import inspect
        update_sig = inspect.signature(indicator.update)
        param_count = len(update_sig.parameters)
        
        n_points = len(data['close'])
        results = []
        
        # Time the indicator
        start = time.perf_counter()
        
        if param_count == 1:
            # Single input (close)
            for value in data['close']:
                result = indicator.update(value)
                results.append(result)
        elif param_count == 2:
            # Two inputs (close, volume)
            for close, volume in zip(data['close'], data['volume']):
                result = indicator.update(close, volume)
                results.append(result)
        elif param_count == 3:
            # Three inputs (high, low, close)
            for high, low, close in zip(data['high'], data['low'], data['close']):
                result = indicator.update(high, low, close)
                results.append(result)
        elif param_count == 4:
            # Four inputs (high, low, close, volume)
            for high, low, close, volume in zip(data['high'], data['low'], data['close'], data['volume']):
                result = indicator.update(high, low, close, volume)
                results.append(result)
        else:
            return {'error': f"Unsupported parameter count: {param_count}", 'success': False}
        
        total_time = time.perf_counter() - start
        per_tick_us = (total_time / n_points) * 1_000_000
        
        return {
            'total_time': total_time,
            'per_tick_us': per_tick_us,
            'final_result': results[-1] if results else None,
            'param_count': param_count,
            'success': True
        }
        
    except Exception as e:
        return {'error': str(e), 'success': False}

def extended_audit():
    """Extended audit of all streaming indicators."""
    print("🔍 EXTENDED STREAMING INDICATOR AUDIT")
    print("=" * 60)
    
    # Generate test data
    data = create_test_data(2000)
    print(f"Test data: {len(data['close'])} points")
    print()
    
    # Get all available streaming indicators
    indicator_classes = []
    
    # Collect all streaming classes from the module
    import ta_numba.streaming as streaming_module
    for name in dir(streaming_module):
        if name.endswith('Streaming') and name != 'StreamingIndicator' and name != 'StreamingIndicatorMultiple':
            try:
                cls = getattr(streaming_module, name)
                if hasattr(cls, 'update'):
                    indicator_classes.append((name, cls))
            except:
                pass
    
    print(f"Found {len(indicator_classes)} streaming indicators:")
    for name, _ in indicator_classes:
        print(f"  - {name}")
    print()
    
    # Test each indicator with default parameters
    results = []
    working_indicators = []
    failed_indicators = []
    
    print("📊 TESTING ALL INDICATORS:")
    print("-" * 50)
    print(f"{'Indicator':<30} {'Status':<10} {'Time (μs)':<12} {'Category'}")
    print("-" * 70)
    
    for name, cls in indicator_classes:
        short_name = name.replace('Streaming', '')
        
        # Try different parameter combinations
        test_configs = [
            ([]),  # No parameters
            ([14]),  # Single parameter
            ([20]),  # Alternative parameter
            ([12, 26, 9]),  # Multiple parameters (MACD)
            ([20, 2.0]),  # Two parameters (BBands)
        ]
        
        success = False
        for config in test_configs:
            try:
                result = test_indicator(cls, data, *config)
                if result['success']:
                    per_tick = result['per_tick_us']
                    
                    # Categorize performance
                    if per_tick < 1.0:
                        category = "✅ FAST"
                    elif per_tick < 5.0:
                        category = "⚠️ MEDIUM"
                    else:
                        category = "❌ SLOW"
                    
                    print(f"{short_name:<30} {'✅ PASS':<10} {per_tick:<12.2f} {category}")
                    
                    results.append({
                        'name': short_name,
                        'class': cls,
                        'per_tick_us': per_tick,
                        'config': config,
                        'param_count': result['param_count']
                    })
                    working_indicators.append(name)
                    success = True
                    break
            except Exception as e:
                continue
        
        if not success:
            print(f"{short_name:<30} {'❌ FAIL':<10} {'N/A':<12} Error")
            failed_indicators.append(name)
    
    # Summary
    print()
    print("🎯 SUMMARY:")
    print("-" * 20)
    print(f"Total indicators found: {len(indicator_classes)}")
    print(f"Working indicators: {len(working_indicators)}")
    print(f"Failed indicators: {len(failed_indicators)}")
    print()
    
    # Performance analysis
    if results:
        results.sort(key=lambda x: x['per_tick_us'])
        
        fast_count = sum(1 for r in results if r['per_tick_us'] < 1.0)
        medium_count = sum(1 for r in results if 1.0 <= r['per_tick_us'] < 5.0)
        slow_count = sum(1 for r in results if r['per_tick_us'] >= 5.0)
        
        print("📈 PERFORMANCE BREAKDOWN:")
        print(f"  Fast (< 1μs): {fast_count} indicators")
        print(f"  Medium (1-5μs): {medium_count} indicators")
        print(f"  Slow (≥ 5μs): {slow_count} indicators")
        print()
        
        # Top and bottom performers
        print("🏆 TOP 5 PERFORMERS:")
        for i, result in enumerate(results[:5]):
            print(f"  {i+1}. {result['name']}: {result['per_tick_us']:.2f}μs")
        
        print()
        print("🔧 BOTTOM 5 PERFORMERS (need optimization):")
        for i, result in enumerate(results[-5:]):
            print(f"  {i+1}. {result['name']}: {result['per_tick_us']:.2f}μs")
    
    # Failed indicators
    if failed_indicators:
        print()
        print("❌ FAILED INDICATORS (need implementation fixes):")
        for name in failed_indicators:
            print(f"  - {name}")
    
    return results, working_indicators, failed_indicators

if __name__ == "__main__":
    results, working, failed = extended_audit()