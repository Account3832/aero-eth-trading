"""Indicators and context for 24/7 crypto. Every feature at row i uses only bars <= i (no look-ahead).

Timestamp convention: a bar's index is its START time (UTC). It is usable from start + 5 minutes (its close).
Higher-timeframe bars (1h, 4h) are built from the 5-minute bars and joined to a 5-minute bar only after that
higher bar has COMPLETED. There is no session open or close: days are UTC days, VWAP is a rolling 24 hours.
"""
from __future__ import annotations

import numpy as np
import pandas as pd



def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False).mean()


def rsi(close: pd.Series, n: int = 14) -> pd.Series:
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    out = 100 - 100 / (1 + up / dn.replace(0, np.nan))
    out = out.where(~((dn == 0) & (up > 0)), 100.0)
    return out.where(~((dn == 0) & (up == 0)), 50.0)


def true_range(h, l, c):
    pc = c.shift()
    return pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)


def atr(h, l, c, n: int = 14):
    return true_range(h, l, c).ewm(alpha=1 / n, adjust=False).mean()


def adx(h, l, c, n: int = 14):
    up, dn = h.diff(), -l.diff()
    pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=h.index)
    mdm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=h.index)
    a = atr(h, l, c, n)
    pdi = 100 * pdm.ewm(alpha=1 / n, adjust=False).mean() / a
    mdi = 100 * mdm.ewm(alpha=1 / n, adjust=False).mean() / a
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi).replace(0, np.nan)
    return dx.ewm(alpha=1 / n, adjust=False).mean()


def bollinger(c: pd.Series, n: int = 20, k: float = 2.0):
    m = c.rolling(n).mean()
    s = c.rolling(n).std(ddof=0)
    return m, m + k * s, m - k * s


def rolling_vwap(df: pd.DataFrame, bars: int = 288) -> pd.Series:
    """VWAP over the last 24 hours (no daily reset in a 24/7 market). NaN where there was no volume."""
    tp = (df.high + df.low + df.close) / 3
    pv = (tp * df.volume).rolling(bars, min_periods=bars // 4).sum()
    v = df.volume.rolling(bars, min_periods=bars // 4).sum()
    return pv / v.replace(0, np.nan)


def _ns(s) -> pd.Series:
    return pd.Series(pd.DatetimeIndex(s).as_unit("ns"), index=s.index)


def htf_bars(df5: pd.DataFrame, minutes: int, prefix: str) -> pd.DataFrame:
    """Higher-timeframe context bars. Index = bar start; `available_at` = when the bar is complete."""
    rs = df5.resample(f"{minutes}min", closed="left", label="left")
    h = rs.agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}).dropna(subset=["close"])
    h["available_at"] = h.index + pd.Timedelta(minutes=minutes)
    c = h.close
    ema20 = ema(c, 20)
    slope = ema20 - ema20.shift(3)
    out = pd.DataFrame({
        "available_at": h["available_at"], f"{prefix}_close": c, f"{prefix}_ema20": ema20, f"{prefix}_slope": slope,
        f"{prefix}_atr": atr(h.high, h.low, c, 14), f"{prefix}_adx": adx(h.high, h.low, c, 14),
        f"{prefix}_dir": np.where((c > ema20) & (slope > 0), 1, np.where((c < ema20) & (slope < 0), -1, 0))}, index=h.index)
    return out


def _join_htf(d: pd.DataFrame, htf: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    left = d[["bar_close"]].copy()
    left["bar_close"] = _ns(left["bar_close"])
    left = left.reset_index(names="ts").sort_values("bar_close")
    right = htf.reset_index(drop=True)
    right["available_at"] = _ns(right["available_at"])
    right = right.sort_values("available_at")
    m = pd.merge_asof(left, right, left_on="bar_close", right_on="available_at", direction="backward")
    m = m.set_index("ts").reindex(d.index)
    return m[cols]


def add_features(bars: pd.DataFrame, ref: pd.DataFrame | None = None, tf: int = 5) -> pd.DataFrame:
    """bars: closed, gap-filled bars at `tf` minutes with a UTC index (use data.resample_bars for tf > 5).
    ref: optional BTC bars at the same tf (market context only)."""
    if bars.index.tz is None:
        raise ValueError("bars index must be timezone-aware (UTC)")
    BARS_DAY = 1440 // tf
    bph = max(60 // tf, 1)
    d = bars.copy().sort_index()
    d.attrs["tf"] = tf
    d["date"] = d.index.date
    d["tod"] = d.index.strftime("%H:%M")
    d["utc_block"] = (d.index.hour // 4 * 4).map(lambda x: f"{x:02d}-{x + 4:02d}h UTC")
    d["bar_close"] = d.index + pd.Timedelta(minutes=tf)
    c, h, l = d.close, d.high, d.low

    d["ema9"], d["ema21"], d["ema50"] = ema(c, 9), ema(c, 21), ema(c, 50)
    d["rsi"] = rsi(c)
    d["atr"] = atr(h, l, c)
    d["adx"] = adx(h, l, c)
    d["bb_mid"], d["bb_up"], d["bb_lo"] = bollinger(c, 20, 2.0)
    _, _, d["bb_lo25"] = bollinger(c, 20, 2.5)
    d["bb_width"] = (d.bb_up - d.bb_lo) / d.bb_mid
    q = d.bb_width.rolling(7 * BARS_DAY, min_periods=2 * BARS_DAY).quantile(0.2).shift(1)   # lowest fifth of the last week
    d["quiet"] = (d.bb_width <= q).fillna(False)
    d["quiet_frac"] = d.quiet.astype(float).rolling(max(bph, 4)).mean().shift(1)         # share of the last hour that was quiet
    d["vwap"] = rolling_vwap(d, BARS_DAY)
    d["hi24"] = h.rolling(BARS_DAY).max().shift(1)      # prior 24h high/low, excluding this bar
    d["lo24"] = l.rolling(BARS_DAY).min().shift(1)
    d["rvol"] = d.volume / d.volume.rolling(BARS_DAY, min_periods=BARS_DAY // 3).median().shift(1).replace(0, np.nan)
    d["ret1h"] = c.pct_change(bph)
    lr = np.log(c).diff()
    d["rv"] = lr.rolling(BARS_DAY).std() * np.sqrt(BARS_DAY * 365)

    cols1 = ["h_close", "h_ema20", "h_slope", "h_atr", "h_adx", "h_dir"]
    d[cols1] = _join_htf(d, htf_bars(d[["open", "high", "low", "close", "volume"]], 60, "h"), cols1)
    cols4 = ["f_close", "f_ema20", "f_slope", "f_atr", "f_adx", "f_dir"]
    d[cols4] = _join_htf(d, htf_bars(d[["open", "high", "low", "close", "volume"]], 240, "f"), cols4)
    d["h_dir"] = d["h_dir"].fillna(0).astype(int)
    d["f_dir"] = d["f_dir"].fillna(0).astype(int)

    # BTC context (read-only): its own 1h trend and its last-hour move, aligned on bar start time
    d["b_dir"], d["b_atr_pct"] = 0, np.nan
    d["b_ret1h"] = np.nan
    if ref is not None and len(ref):
        r = ref.reindex(d.index).ffill()
        rc = r.close
        d["b_ret1h"] = rc.pct_change(bph)
        d["b_atr_pct"] = atr(r.high, r.low, rc).div(rc) * np.sqrt(bph)      # typical 1h move
        bh = htf_bars(ref[["open", "high", "low", "close", "volume"]], 60, "b")
        d["b_dir"] = _join_htf(d, bh, ["b_dir"])["b_dir"].fillna(0).astype(int)

    d["regime"] = np.where((d.adx >= 22) & (d.h_dir != 0), "trend", np.where(d.adx < 18, "range", "transition"))
    med = d["atr"].rolling(BARS_DAY * 20, min_periods=BARS_DAY).median()
    d["vol_regime"] = np.where(d.atr > 1.25 * med, "expanding", np.where(d.atr < 0.8 * med, "contracting", "normal"))
    from .levels import add_structure
    return add_structure(d, 4, 4)       # confirmed swing highs/lows and trend structure (causal)
