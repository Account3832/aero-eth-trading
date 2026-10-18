import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

from cryptoai.backtest import resolve_trade, run_research, simulate
from cryptoai.config import Settings
from cryptoai.data import fill_gaps, resample_bars
from cryptoai.features import add_features
from cryptoai.paper import CryptoLedger, size_position
from cryptoai.strategies import REGISTRY
from tests.synth import make_bars


def _feats(days=120, seed=1, tf=15):
    b = make_bars(days, seed=seed)
    r = make_bars(days, seed=seed + 50, price=60000)
    return add_features(resample_bars(b, tf), resample_bars(r, tf), tf=tf)


def test_fill_gaps_adds_flat_candles():
    b = make_bars(2)
    holes = b.drop(b.index[10:13])
    f = fill_gaps(holes)
    assert len(f) == len(b)
    assert (f.iloc[10:13].volume == 0).all()
    assert (f.iloc[10:13].open == f.iloc[9].close).all()


def test_resample_keeps_only_complete_bars():
    b = make_bars(2).iloc[:-1]            # last 15m bar is incomplete (2 of 3 five-minute bars)
    r = resample_bars(b, 15)
    assert r.index[-1] + pd.Timedelta(minutes=15) <= b.index[-1] + pd.Timedelta(minutes=5)


def test_features_no_lookahead():
    """Features at time t must not change when future bars are removed."""
    b = make_bars(60)
    full = add_features(resample_bars(b, 15), tf=15)
    cut = b.iloc[: 288 * 40]
    part = add_features(resample_bars(cut, 15), tf=15)
    cols = ["ema21", "rsi", "atr", "adx", "vwap", "h_dir", "f_dir", "rvol", "hi24"]
    common = part.index[-200:]
    a, c = part.loc[common, cols], full.loc[common, cols]
    assert np.allclose(a.fillna(-1).values, c.fillna(-1).values, atol=1e-9)


def test_resolve_trade_stop_wins_ambiguous_bar():
    o = np.array([100, 100, 100.0]); h = np.array([100, 110, 100.0]); l = np.array([100, 90, 100.0]); c = o.copy()
    r = resolve_trade(o, h, l, c, 1, 100, 100, 5, 95, 105, 110, 0, 10)
    assert r["net"] < 0 and r["reasons"][1] == "stop"


def test_resolve_trade_target_needs_both_halves():
    o = np.array([100, 100, 100, 100.0]); h = np.array([100, 106, 111, 100.0]); l = np.array([100, 99, 101, 100.0]); c = o.copy()
    r = resolve_trade(o, h, l, c, 1, 100, 100, 5, 95, 105, 110, 0, 10)
    assert r["reasons"] == {1: "T1", 2: "T2"} and abs(r["net"] - 7.5) < 1e-9


def test_simulate_costs_reduce_results():
    d = _feats()
    s = Settings()
    free = Settings(fee_pct=0.0, slip_pct_eth=0.0)
    a = simulate(d, REGISTRY["donchian_breakout"](), s, "ETH-USD")
    b = simulate(d, REGISTRY["donchian_breakout"](), free, "ETH-USD")
    if len(a) and len(b):
        assert a.net_R.mean() < b.net_R.mean()


def test_every_strategy_runs_and_is_long_only():
    d = _feats()
    s = Settings()
    for n in (*s.enabled_strategies, *s.research_only_strategies):
        sig = REGISTRY[n]().signals(d)
        assert set(sig["dir"].unique()) <= {0, 1}


def test_run_research_report_shape():
    d = _feats(150)
    rep = run_research(d, Settings(), "ETH-USD")
    assert set(rep["strategies"]) >= {"trend_pullback", "donchian_breakout"}
    for r in rep["strategies"].values():
        assert r["verdict"] in ("NOT_DEMONSTRATED", "INSUFFICIENT_SAMPLE", "FAILED_OOS", "EDGE_SUPPORTED", "UNDERLYING_EDGE_SUPPORTED")
        assert "cost_sensitivity_out_of_sample" in r


def test_size_position_caps_at_account():
    s = Settings()
    p = size_position(s, "ETH-USD", 2000.0, 1.0)      # wants 50 ETH = $100k, must be capped
    assert p["notional_usd"] <= s.account_equity and p["capped"]
    q = size_position(s, "ETH-USD", 2000.0, 40.0)
    assert abs(q["risk_usd"] - s.risk_usd) < 2


def test_ledger_is_idempotent_and_closes():
    d = _feats(30)
    s = Settings()
    with tempfile.TemporaryDirectory() as t:
        led = CryptoLedger(s, Path(t), "ETH-USD")
        i = len(d) - 40
        plan = {"strategy": "trend_pullback", "label": "x", "signal_time": str(d.index[i]), "atr": float(d.atr.iloc[i]), "stop_atr": 1.5,
                "t1_r": 1.5, "t2_r": 3.0, "max_hold_hours": 2.0, "units": 1.0, "regime": "x"}
        assert led.open_position(plan) is True
        assert led.open_position(plan) is False
        ev = led.update(d, pd.Timestamp.now(tz="UTC"))
        ev2 = led.update(d, pd.Timestamp.now(tz="UTC"))
        assert any(e["type"].startswith("EXIT") for e in ev)      # 2h max hold must have passed inside 40 bars
        assert ev2 == [] and len(led.closed()) == 1 and led.positions() == []
