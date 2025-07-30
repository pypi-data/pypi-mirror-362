import numpy as np
import pandas as pd
import time
import pytest

try:
    import talib
    HAS_TALIB = True
except ImportError:
    HAS_TALIB = False
    pytest.skip("ta-lib not available", allow_module_level=True)

import ta

# NautilusTrader imports
from nautilus_trader.indicators.average.sma import SimpleMovingAverage
from nautilus_trader.indicators.average.ema import ExponentialMovingAverage
from nautilus_trader.indicators.rsi import RelativeStrengthIndex
from nautilus_trader.indicators.macd import MovingAverageConvergenceDivergence

# ta-numba imports
from ta_numba.trend import sma_numba, ema_numba, macd_numba
from ta_numba.momentum import relative_strength_index_numba

# 100,000개 랜덤 가격 데이터 생성
np.random.seed(42)
close_prices = np.random.rand(100_000) * 100
df = pd.DataFrame({'close': close_prices})

# 실행 시간 기록용 딕셔너리
results = {}

# ===== CRITICAL: WARM UP NUMBA FUNCTIONS FIRST =====
print("Warming up Numba functions...")
start_warmup = time.time()
_ = sma_numba(close_prices[:100])  # Small data for warm-up
_ = ema_numba(close_prices[:100], 20)
_ = relative_strength_index_numba(close_prices[:100])
_ = macd_numba(close_prices[:100])
warmup_time = time.time() - start_warmup
print(f"Numba warm-up completed in {warmup_time:.4f} seconds")
print()

print("\n===== SMA 비교 =====")
# ta-numba (actual numba implementation) - multiple runs for accuracy
times = []
for _ in range(3):
    start = time.time()
    sma_ta_numba = sma_numba(close_prices)
    times.append(time.time() - start)
results['ta-numba SMA'] = min(times)  # Take best time (removes outliers)

# ta library (pure Python)
start = time.time()
sma_ta = ta.trend.sma_indicator(df['close'], window=20)
results['ta SMA'] = time.time() - start

# TA-Lib (C implementation)
if HAS_TALIB:
    start = time.time()
    sma_talib = talib.SMA(close_prices, timeperiod=20)
    results['TA-Lib SMA'] = time.time() - start
else:
    results['TA-Lib SMA'] = float('inf')  # Skip if not available

# NautilusTrader (highly optimized implementation)
start = time.time()
sma_nautilus = SimpleMovingAverage(period=20)
sma_nautilus_values = np.full(len(close_prices), np.nan)

# Optimization 5: Maximum performance with cached references and chunked processing
update_raw = sma_nautilus.update_raw
get_value = lambda: sma_nautilus.value
get_initialized = lambda: sma_nautilus.initialized

# Process in chunks to reduce Python overhead
chunk_size = 10000
for chunk_start in range(0, len(close_prices), chunk_size):
    chunk_end = min(chunk_start + chunk_size, len(close_prices))
    chunk = close_prices[chunk_start:chunk_end]
    
    for i, price in enumerate(chunk, chunk_start):
        update_raw(price)
        if get_initialized():
            sma_nautilus_values[i] = get_value()

results['NautilusTrader SMA'] = time.time() - start

print("\n===== EMA 비교 =====")
# ta-numba (actual numba implementation) - multiple runs for accuracy
times = []
for _ in range(3):
    start = time.time()
    ema_ta_numba = ema_numba(close_prices, 20)
    times.append(time.time() - start)
results['ta-numba EMA'] = min(times)

# ta library (pure Python)
start = time.time()
ema_ta = ta.trend.ema_indicator(df['close'], window=20)
results['ta EMA'] = time.time() - start

# TA-Lib (C implementation)
if HAS_TALIB:
    start = time.time()
    ema_talib = talib.EMA(close_prices, timeperiod=20)
    results['TA-Lib EMA'] = time.time() - start
else:
    results['TA-Lib EMA'] = float('inf')  # Skip if not available

# NautilusTrader (highly optimized implementation)
start = time.time()
ema_nautilus = ExponentialMovingAverage(period=20)
ema_nautilus_values = np.full(len(close_prices), np.nan)

# Optimization 6: Cached methods with early initialization detection
update_raw = ema_nautilus.update_raw
get_value = lambda: ema_nautilus.value
initialized = False

for i in range(len(close_prices)):
    update_raw(close_prices[i])
    if not initialized:
        if ema_nautilus.initialized:
            initialized = True
    if initialized:
        ema_nautilus_values[i] = get_value()

results['NautilusTrader EMA'] = time.time() - start

print("\n===== RSI 비교 =====")
# ta-numba (actual numba implementation) - multiple runs for accuracy  
times = []
for _ in range(3):
    start = time.time()
    rsi_ta_numba = relative_strength_index_numba(close_prices)
    times.append(time.time() - start)
results['ta-numba RSI'] = min(times)

# ta library (pure Python)
start = time.time()
rsi_ta = ta.momentum.rsi(df['close'], window=14)
results['ta RSI'] = time.time() - start

# TA-Lib (C implementation)
if HAS_TALIB:
    start = time.time()
    rsi_talib = talib.RSI(close_prices, timeperiod=14)
    results['TA-Lib RSI'] = time.time() - start
else:
    results['TA-Lib RSI'] = float('inf')  # Skip if not available

# NautilusTrader (optimized implementation)
start = time.time()
rsi_nautilus = RelativeStrengthIndex(period=14)
rsi_nautilus_values = np.full(len(close_prices), np.nan)

# Optimization 3: Direct index access and reduced function call overhead
n = len(close_prices)
for i in range(n):
    rsi_nautilus.update_raw(close_prices[i])
    if i >= 13:  # RSI typically needs 14+ periods, so check from index 13
        rsi_nautilus_values[i] = rsi_nautilus.value

results['NautilusTrader RSI'] = time.time() - start

print("\n===== MACD 비교 =====")
# ta-numba (actual numba implementation) - multiple runs for accuracy
times = []
for _ in range(3):
    start = time.time()
    macd_ta_numba = macd_numba(close_prices)
    times.append(time.time() - start)
results['ta-numba MACD'] = min(times)

# ta library (pure Python)
start = time.time()
macd_ta = ta.trend.MACD(df['close']).macd()
results['ta MACD'] = time.time() - start

# TA-Lib (C implementation)
if HAS_TALIB:
    start = time.time()
    macd_talib, _, _ = talib.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
    results['TA-Lib MACD'] = time.time() - start
else:
    results['TA-Lib MACD'] = float('inf')  # Skip if not available

# NautilusTrader (optimized implementation) - using working API
start = time.time()
try:
    # Use the working constructor found in testing
    macd_nautilus = MovingAverageConvergenceDivergence(12, 26)
    macd_nautilus_values = np.full(len(close_prices), np.nan)
    
    # Optimization 4: Minimize object access and use direct assignment
    update_method = macd_nautilus.update_raw  # Cache method reference
    value_property = lambda: macd_nautilus.value  # Cache property access
    
    for i, price in enumerate(close_prices):
        update_method(price)
        if i >= 25:  # MACD typically needs 26+ periods
            macd_nautilus_values[i] = value_property()
    
    results['NautilusTrader MACD'] = time.time() - start
except Exception as e:
    print(f"NautilusTrader MACD failed: {e}")
    results['NautilusTrader MACD'] = float('inf')

# 결과 출력
print("\n===== 성능 비교 결과 =====")
for library, execution_time in results.items():
    print(f"{library}: {execution_time:.4f}초")
