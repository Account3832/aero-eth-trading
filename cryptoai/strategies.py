"""Crypto-specific, long-only (spot) hypotheses. These are RESEARCH CANDIDATES, not assumed winners.

They use behaviour that is specific to the crypto market: 24/7 trading with no open, close or overnight gap, strong
trend persistence, volatility clusters (quiet squeezes followed by fast moves), forced-liquidation wicks that snap back,
and BTC leading the smaller coins. Stock ideas that depend on a market open (opening-range breakouts, gap fades,
prior-close levels, a 15:45 exit) are deliberately NOT used.

A signal is produced at a bar's CLOSE. The backtester and the paper ledger enter at the NEXT bar's open plus slippage.
Nothing here has been shown to make money: each strategy must pass the fair test (see backtest.py) before it is trusted.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

FILTER_TEXT = {
    "htf": "the 1-hour trend is not up",
    "f4": "the 4-hour trend is down",
    "btc": "Bitcoin's 1-hour trend is down",
    "adx": "the trend is too weak (ADX under 20)",
    "rvol": "trading volume is below normal",
    "vwap": "price is below the 24-hour average price (VWAP)",
}


@dataclass(frozen=True)
class StrategySpec:
    name: str
    version: str
    hypothesis: str
    why_crypto: str
    trigger: str
    stop_logic: str
    targets: str
    holding: str
    params: dict = field(default_factory=dict)


class Strategy:
    spec: StrategySpec
    default_filters: tuple = ()
    stop_atr = 1.5
    t1_r = 1.5
    t2_r = 3.0
    max_hold_hours = 6.0
    needs_chart = False      # True = also needs the multi-scale chart checklist and chart-based exits (backtester and live monitor apply them)
    min_room_r = None        # for needs_chart strategies: minimum room to resistance, in R

    def __init__(self, filters=None, stop_atr=None, t1_r=None, t2_r=None, **params):
        self.filters = tuple(self.default_filters if filters is None else filters)
        if stop_atr is not None:
            self.stop_atr = stop_atr
        if t1_r is not None:
            self.t1_r = t1_r
        if t2_r is not None:
            self.t2_r = t2_r
        self.params = {**self.spec.params, **params}

    @property
    def name(self) -> str:
        return self.spec.name

    def label(self) -> str:
        p = {**self.params, "stop_atr": self.stop_atr, "t1_r": self.t1_r, "t2_r": self.t2_r, "filters": list(self.filters),
             "max_hold_h": self.max_hold_hours}
        return f"{self.name}@{self.spec.version}#{hashlib.sha1(json.dumps(p, sort_keys=True).encode()).hexdigest()[:8]}"

    @property
    def blended_rr(self) -> float:
        return 0.5 * self.t1_r + 0.5 * self.t2_r

    def raw(self, d: pd.DataFrame) -> tuple[pd.Series, str]:
        raise NotImplementedError

    def masks(self, d: pd.DataFrame) -> dict[str, pd.Series]:
        return {"htf": d.h_dir == 1, "f4": d.f_dir >= 0, "btc": d.b_dir >= 0, "adx": d.adx >= 20, "rvol": d.rvol >= 1.0,
                "vwap": d.close > d.vwap}

    def signals(self, d: pd.DataFrame) -> pd.DataFrame:
        longs, trig = self.raw(d)
        longs = longs.fillna(False)
        m = self.masks(d)
        for f in self.filters:
            longs = longs & m[f].fillna(False)
        longs = longs & d.atr.notna()
        return pd.DataFrame({"dir": np.where(longs, 1, 0), "trigger": np.where(longs, trig, "")}, index=d.index)

    def blockers(self, d: pd.DataFrame) -> list[str]:
        """If the trigger candle is present on the last bar, which filters stopped it. Empty = trigger not present."""
        longs, _ = self.raw(d)
        if not bool(longs.fillna(False).iloc[-1]):
            return []
        m = self.masks(d)
        return [FILTER_TEXT[f] for f in self.filters if not bool(m[f].fillna(False).iloc[-1])]


class TrendPullback(Strategy):
    spec = StrategySpec(
        "trend_pullback", "1.0",
        "When the 1-hour and 4-hour trends are up, a shallow dip to the 21-bar average that is bought back tends to continue up.",
        "Crypto trends persist for hours to days, and dips in a trend are bought quickly because the market never closes.",
        "close of the candle above the prior candle's high after touching the 21-bar average, with the 1h and 4h trend up and Bitcoin not falling.",
        "1.5 x ATR below entry.", "Half at 1.5R, half at 3R (stop to entry after the first).", "30 minutes to 6 hours")
    default_filters = ("htf", "f4", "btc", "adx")

    def raw(self, d):
        touched = d.low.rolling(6).min() <= d.ema21
        longs = (d.ema9 > d.ema21) & touched & (d.close > d.ema21) & (d.close > d.high.shift()) & (d.close > d.open)
        return longs, "dip to the 21-bar average bought back"


class DonchianBreakout(Strategy):
    spec = StrategySpec(
        "donchian_breakout", "1.0",
        "A strong close above the highest price of the last 24 hours, on heavy volume, tends to keep running.",
        "Crypto momentum is persistent, and with no market close, breakouts are not erased by an overnight gap-and-fade.",
        "First candle close above the prior 24-hour high, closing in the top 30% of its range, with volume at least 1.5x normal.",
        "2 x ATR below entry (breakouts need room).", "Half at 1.5R, half at 3R.", "1 to 12 hours")
    default_filters = ("htf", "btc")
    stop_atr = 2.0
    max_hold_hours = 12.0

    def raw(self, d):
        first = (d.close > d.hi24) & (d.close.shift() <= d.hi24.shift())
        strong = (d.close - d.low) >= 0.7 * (d.high - d.low)
        return first & strong & (d.rvol >= 1.5), "first close above the prior 24h high on heavy volume"


class SqueezeBreakout(Strategy):
    spec = StrategySpec(
        "squeeze_breakout", "1.0",
        "After an unusually quiet stretch, price often breaks out fast. Buy the first strong close above the upper band.",
        "Crypto volatility comes in clusters: long quiet squeezes are followed by sharp moves.",
        "Price range in the quietest fifth of the last week for most of the last hour (or last four candles), then a close above the upper Bollinger band on above-normal volume.",
        "1.5 x ATR below entry.", "Half at 1.5R, half at 3R.", "30 minutes to 6 hours")
    default_filters = ("btc", "f4")

    def raw(self, d):
        was_quiet = d.quiet_frac >= 0.75
        return was_quiet & (d.close > d.bb_up) & (d.rvol >= 1.3) & (d.close > d.open), "breakout from a volatility squeeze"


class OversoldBounce(Strategy):
    spec = StrategySpec(
        "oversold_bounce", "1.0",
        "A sudden flush far below the normal range snaps back once price turns up (forced sellers are done).",
        "Leveraged liquidations create fast wicks well outside the normal range that often retrace within hours.",
        "A bar pierced the lower 2.5-sigma band with RSI under 30 in the last 3 bars, then a close above the prior high and above its own open. Not taken in a 4-hour downtrend.",
        "1.5 x ATR below entry.", "Half at 1R, half at 2R (mean reversion takes quicker profits).", "15 minutes to 4 hours")
    default_filters = ("f4",)
    t1_r, t2_r, max_hold_hours = 1.0, 2.0, 4.0

    def raw(self, d):
        flush = ((d.low < d.bb_lo25) & (d.rsi < 30)).astype(float).rolling(3).max().shift(1) > 0
        return flush & (d.close > d.open) & (d.close > d.high.shift()), "bounce after a liquidation-style flush"


class RangeBounce(Strategy):
    spec = StrategySpec(
        "range_bounce", "1.0",
        "In a sideways market, a dip under the lower band that closes back inside tends to return to the middle.",
        "Crypto spends long stretches in ranges between big moves; weekends in particular can be quiet and range-bound.",
        "1-hour ADX under 20, a dip under the lower Bollinger band, a close back above it, RSI under 40, and a green candle.",
        "1.2 x ATR below entry.", "Half at 1R, half at 2R.", "15 minutes to 3 hours")
    t1_r, t2_r, max_hold_hours, stop_atr = 1.0, 2.0, 3.0, 1.2

    def raw(self, d):
        longs = (d.h_adx < 20) & (d.low <= d.bb_lo) & (d.close > d.bb_lo) & (d.rsi < 40) & (d.close > d.open)
        return longs, "range-bottom bounce"


class BtcLead(Strategy):
    spec = StrategySpec(
        "btc_lead", "1.0",
        "When Bitcoin makes a big move up and the coin has barely moved yet, the coin tends to catch up.",
        "Bitcoin leads the rest of the crypto market; smaller coins often follow with a delay.",
        "Bitcoin's last-hour gain is at least 1.5x its typical hour while this coin gained under 40% of that, on a green candle.",
        "1.5 x ATR below entry.", "Half at 1R, half at 2R.", "15 minutes to 2 hours")
    t1_r, t2_r, max_hold_hours = 1.0, 2.0, 2.0

    def raw(self, d):
        big = d.b_ret1h >= 1.5 * d.b_atr_pct
        lag = d.ret1h < 0.4 * d.b_ret1h
        cond = (big & lag & (d.close > d.open) & (d.b_dir >= 0)).fillna(False)
        return cond & ~cond.shift(1, fill_value=False), "coin lagging a strong Bitcoin move"


class SupportBounce(Strategy):
    spec = StrategySpec(
        "support_bounce", "1.0",
        "In an uptrend (higher highs and higher lows), price that dips back to the last higher low and is rejected tends to resume up.",
        "Classic chart support. Crypto trends persist and dips to prior swing lows are widely watched, so reactions there are common.",
        "Uptrend structure on the entry chart and the 1h chart; a candle dips to within a quarter ATR of the last swing low "
        "(never more than one ATR below it) and closes back above it in the top part of its range.",
        "1.5 x ATR below entry.", "Half at 1.5R, half at 3R.", "1 to 6 hours")
    default_filters = ("htf", "btc")

    def raw(self, d):
        a = d.atr
        touch = (d.low <= d.sw_lo + 0.25 * a) & (d.low >= d.sw_lo - 1.0 * a)
        reject = (d.close > d.open) & (d.close > d.sw_lo + 0.25 * a) & ((d.close - d.low) >= 0.6 * (d.high - d.low))
        cond = ((d.sw_trend == 1) & touch & reject).fillna(False)
        return cond & ~cond.shift(1, fill_value=False), "bounce off the last higher low inside an uptrend"


class SwingBreakout(Strategy):
    spec = StrategySpec(
        "swing_breakout", "1.0",
        "A strong close above the last confirmed swing high, on above-normal volume, in an uptrend, tends to continue.",
        "Classic breakout above resistance. Stops resting above swing highs add fuel when they are taken out.",
        "First candle close above the last confirmed swing high, in the top 30% of its range, volume at least 1.3x normal, "
        "and the entry-chart structure is not a downtrend.",
        "2 x ATR below entry.", "Half at 1.5R, half at 3R.", "1 to 8 hours")
    default_filters = ("htf", "btc")
    stop_atr = 2.0
    max_hold_hours = 8.0

    def raw(self, d):
        lvl = d.sw_hi.shift(1)
        first = (d.close > lvl) & (d.close.shift() <= lvl)
        strong = (d.close - d.low) >= 0.7 * (d.high - d.low)
        return (first & strong & (d.rvol >= 1.3) & (d.sw_trend >= 0)).fillna(False), "first strong close above the last swing high"


class ZoneRejection(Strategy):
    """Trader-style checklist: a rejection candle at a STRONG support zone, with the bigger trend up, room to run, and a stop behind the zone.
    The candle test is cheap and runs on every bar; the chart checklist (levels.confluence_check) and the chart-based exits are applied
    by the backtester and the live monitor, because they need the multi-scale chart analysis as of that candle."""
    spec = StrategySpec(
        "zone_rejection", "1.0",
        "A candle that dips into a strong support zone and is rejected, while the bigger trend is up and there is room to run, tends to bounce.",
        "How chart traders actually use support: only strong zones, only with the bigger trend, only with a rejection candle, stop behind the zone.",
        "Bullish rejection candle (closes in the top 40% of its range, lower wick at least 40% of range, range at least 0.8 ATR) while the 1-hour trend is up; "
        "then the chart checklist must pass: bigger trend up, strong support zone touched, entry within 1.5 ATR of it.",
        "Just below the support zone (chart-based).", "Just under the next resistance zones; at least 2R of room is required.", "1 to 12 hours")
    default_filters = ("htf", "btc")
    needs_chart = True
    min_room_r = 2.0
    max_hold_hours = 12.0

    def raw(self, d):
        rng = (d.high - d.low)
        pos = (d.close - d.low) / rng.where(rng > 0)
        wick = (d[["open", "close"]].min(axis=1) - d.low) / rng.where(rng > 0)
        cond = ((d.close > d.open) & (pos >= 0.6) & (wick >= 0.4) & (rng >= 0.8 * d.atr)).fillna(False)
        return cond, "rejection candle at support"


class SteadyScalper(TrendPullback):
    """A deliberate demonstration of the high-win-rate trap: tiny targets, wide stop. Comparison only, never traded."""
    spec = StrategySpec(
        "steady_scalper", "1.0",
        "Same entries as the trend pullback, but with tiny targets and a wide stop to win most trades.",
        "Shows why a high win rate alone does not mean making money: many small wins can be erased by a few large losses.",
        "Same as trend_pullback.", "2.5 x ATR below entry.", "Half at 0.4R, half at 0.8R.", "15 minutes to 3 hours")
    stop_atr, t1_r, t2_r, max_hold_hours = 2.5, 0.4, 0.8, 3.0


class Baseline1hTrend(Strategy):
    """Deliberately simple comparison: one long a day at 12:00 UTC if the 1-hour and 4-hour trends are up."""
    spec = StrategySpec(
        "baseline_1h_trend", "1.0", "Comparison only: does anything beat doing almost nothing?",
        "A fair yardstick for the real strategies.", "One long at 12:00 UTC when the 1h trend is up and the 4h trend is not down.",
        "1.5 x ATR.", "Half at 1.5R, half at 3R.", "Up to 6 hours")

    def raw(self, d):
        at = d.bar_close.dt.strftime("%H:%M") == "12:00"
        return at & (d.h_dir == 1) & (d.f_dir >= 0), "baseline: one trend-direction long at 12:00 UTC"


REGISTRY = {c.spec.name: c for c in (TrendPullback, DonchianBreakout, SqueezeBreakout, OversoldBounce, RangeBounce, BtcLead,
                                     SupportBounce, SwingBreakout, SteadyScalper, ZoneRejection)}
BASELINE = Baseline1hTrend


def build(names, **overrides):
    return [REGISTRY[n](**overrides.get(n, {})) for n in names]
