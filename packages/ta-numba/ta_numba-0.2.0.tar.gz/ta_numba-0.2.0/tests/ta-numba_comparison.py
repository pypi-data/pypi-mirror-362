import timeit
import numpy as np
import pandas as pd

# Import functions from the ta-numba library
from ta_numba.trend import sma_numba, ema_numba, macd_numba
from ta_numba.momentum import relative_strength_index_numba as rsi_numba
from ta_numba.volatility import average_true_range_numba as atr_numba, bollinger_bands_numba as bb_numba
from ta_numba.helpers import _ema_numba_unadjusted as ema_helper_numba # ATR and RSI depend on this helper

# --- Pandas/Numpy Implementations ---
# These mimic the logic used in popular libraries like `ta`

def sma_pandas(series: np.ndarray, period: int) -> float:
    if len(series) < period:
        return np.nan
    return np.mean(series[-period:])

def ema_pandas(series: pd.Series, period: int) -> float:
    if len(series) < period:
        return np.nan
    # pandas.ewm is slow for single-value updates, but it's the standard
    return series.ewm(span=period, adjust=False).mean().iloc[-1]

def rsi_pandas(series: pd.Series, period: int) -> float:
    if len(series) <= period:
        return np.nan
    delta = series.diff()
    gain = delta.where(delta > 0, 0).dropna()
    loss = -delta.where(delta < 0, 0).dropna()
    
    # Using ewm for the rolling average of gains and losses
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean().iloc[-1]
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean().iloc[-1]
    
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))

def atr_pandas(high: pd.Series, low: pd.Series, close: pd.Series, period: int) -> float:
    if len(high) <= period:
        return np.nan
    tr = pd.Series(np.maximum(high.iloc[1:].values - low.iloc[1:].values,
                              np.abs(high.iloc[1:].values - close.iloc[:-1].values),
                              np.abs(low.iloc[1:].values - close.iloc[:-1].values)),
                   index=high.index[1:])
    return tr.ewm(alpha=1/period, adjust=False).mean().iloc[-1]

def macd_pandas(series: pd.Series, period_fast: int, period_slow: int) -> float:
    if len(series) < period_slow:
        return np.nan
    ema_fast = series.ewm(span=period_fast, adjust=False).mean()
    ema_slow = series.ewm(span=period_slow, adjust=False).mean()
    return (ema_fast - ema_slow).iloc[-1]

def bb_pandas(series: pd.Series, period: int, std_dev: float):
    if len(series) < period:
        return np.nan, np.nan, np.nan
    rolling_mean = series.rolling(window=period).mean().iloc[-1]
    rolling_std = series.rolling(window=period).std().iloc[-1]
    hband = rolling_mean + (rolling_std * std_dev)
    lband = rolling_mean - (rolling_std * std_dev)
    return hband, lband, rolling_mean

# --- Benchmark Setup ---

# Generate synthetic streaming data
np.random.seed(42)
STREAM_SIZE = 1000
INITIAL_PRICE = 100.0
ohlc_data = {
    'open': INITIAL_PRICE + np.random.randn(STREAM_SIZE).cumsum(),
    'high': INITIAL_PRICE + np.random.randn(STREAM_SIZE).cumsum() + 0.5,
    'low': INITIAL_PRICE + np.random.randn(STREAM_SIZE).cumsum() - 0.5,
    'close': INITIAL_PRICE + np.random.randn(STREAM_SIZE).cumsum(),
}
ohlc_data['high'] = np.maximum(ohlc_data['high'], ohlc_data['close'])
ohlc_data['low'] = np.minimum(ohlc_data['low'], ohlc_data['close'])

# Indicator parameters
SMA_P, EMA_P, RSI_P = 14, 14, 14
BB_P, BB_STD = 20, 2
ATR_P = 14
MACD_FAST, MACD_SLOW = 12, 26

# --- JIT WARM-UP ---
print("Warming up Numba JIT compilers...")
close_warmup = ohlc_data['close'][:50]
high_warmup = ohlc_data['high'][:50]
low_warmup = ohlc_data['low'][:50]

_ = sma_numba(close_warmup)
_ = ema_numba(close_warmup, EMA_P)
_ = rsi_numba(close_warmup)
_ = bb_numba(close_warmup, BB_P, BB_STD)
_ = atr_numba(high_warmup, low_warmup, close_warmup)
_ = macd_numba(close_warmup)
_ = ema_helper_numba(close_warmup, EMA_P) # Helper for RSI/ATR
print("Warm-up complete.\n")


# --- Streaming Simulation ---
def run_streaming_benchmark():
    # Use lists to append data tick-by-tick, simulating a stream
    close_stream = list(ohlc_data['close'][:BB_P + 1])
    high_stream = list(ohlc_data['high'][:BB_P + 1])
    low_stream = list(ohlc_data['low'][:BB_P + 1])
    
    numba_times = {k: 0.0 for k in ['SMA', 'EMA', 'RSI', 'BB', 'ATR', 'MACD']}
    pandas_times = {k: 0.0 for k in ['SMA', 'EMA', 'RSI', 'BB', 'ATR', 'MACD']}
    
    num_ticks = STREAM_SIZE - (BB_P + 1)

    for i in range(BB_P + 1, STREAM_SIZE):
        # Append new tick
        close_stream.append(ohlc_data['close'][i])
        high_stream.append(ohlc_data['high'][i])
        low_stream.append(ohlc_data['low'][i])
        
        # Convert to numpy/pandas for the functions
        # This conversion overhead is part of the test
        close_np = np.array(close_stream, dtype=float)
        close_pd = pd.Series(close_np)
        high_pd = pd.Series(np.array(high_stream, dtype=float))
        low_pd = pd.Series(np.array(low_stream, dtype=float))

        # --- Benchmark Numba ---
        numba_times['SMA'] += timeit.timeit(lambda: sma_numba(close_np), number=1)
        numba_times['EMA'] += timeit.timeit(lambda: ema_numba(close_np, EMA_P), number=1)
        numba_times['RSI'] += timeit.timeit(lambda: rsi_numba(close_np), number=1)
        numba_times['BB'] += timeit.timeit(lambda: bb_numba(close_np, BB_P, BB_STD), number=1)
        numba_times['ATR'] += timeit.timeit(lambda: atr_numba(np.array(high_stream), np.array(low_stream), np.array(close_stream)), number=1)
        numba_times['MACD'] += timeit.timeit(lambda: macd_numba(close_np), number=1)

        # --- Benchmark Pandas ---
        pandas_times['SMA'] += timeit.timeit(lambda: sma_pandas(close_np, SMA_P), number=1)
        pandas_times['EMA'] += timeit.timeit(lambda: ema_pandas(close_pd, EMA_P), number=1)
        pandas_times['RSI'] += timeit.timeit(lambda: rsi_pandas(close_pd, RSI_P), number=1)
        pandas_times['BB'] += timeit.timeit(lambda: bb_pandas(close_pd, BB_P, BB_STD), number=1)
        pandas_times['ATR'] += timeit.timeit(lambda: atr_pandas(high_pd, low_pd, close_pd, ATR_P), number=1)
        pandas_times['MACD'] += timeit.timeit(lambda: macd_pandas(close_pd, MACD_FAST, MACD_SLOW), number=1)

    print("--- Streaming Benchmark Results ---")
    print(f"Averaged over {num_ticks} streaming ticks.\n")
    print(f"{'Indicator':<10} | {'Numba (µs)':<15} | {'Pandas (µs)':<15} | {'Speedup':<10}")
    print("-" * 60)
    
    for indicator in numba_times:
        avg_numba_us = (numba_times[indicator] / num_ticks) * 1e6
        avg_pandas_us = (pandas_times[indicator] / num_ticks) * 1e6
        speedup = avg_pandas_us / avg_numba_us
        
        print(f"{indicator:<10} | {avg_numba_us:<15.2f} | {avg_pandas_us:<15.2f} | {speedup:.2f}x")

if __name__ == '__main__':
    run_streaming_benchmark()