"""Synthetic 5-minute candles for tests (random walk with volatility clustering)."""
import numpy as np
import pandas as pd


def make_bars(days=200, start="2025-01-01", seed=1, price=100.0, vol=0.0015) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    idx = pd.date_range(start, periods=days * 288, freq="5min", tz="UTC")
    v = vol * (1 + 0.8 * np.sin(np.arange(len(idx)) / 4000.0) ** 2)
    ret = rng.normal(0.00001, v)
    close = price * np.exp(np.cumsum(ret))
    open_ = np.r_[price, close[:-1]]
    spread = np.abs(rng.normal(0, v)) * close
    high = np.maximum(open_, close) + spread
    low = np.minimum(open_, close) - spread
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": rng.uniform(1, 50, len(idx))}, index=idx)
