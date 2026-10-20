import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

from cryptoai import levels as L
from cryptoai import runner
from cryptoai.backtest import compare_exits, run_research, simulate
from cryptoai.config import Settings
from cryptoai.data import resample_bars
from cryptoai.features import add_features
from cryptoai.monitor import scan, signal_text
from cryptoai.paper import CryptoLedger
from cryptoai.strategies import REGISTRY
from tests.synth import make_bars


def Z(lo, hi, strength, role):
    return {"low": lo, "high": hi, "mid": (lo + hi) / 2, "strength": strength, "role": role, "touches": 3}


A = {"ok": True, "zones": [Z(98, 98.8, "Moderate", "support"), Z(106, 107, "Strong", "resistance"), Z(111, 112, "Moderate", "resistance"), Z(115, 116, "Weak", "resistance")]}


def test_structure_plan_long_uses_zones():
    p = L.structure_plan(A, 100.0, 1.5, True)
    assert p["ok"] and abs(p["stop"] - 97.625) < 1e-9 and abs(p["t1"] - 105.85) < 1e-9 and abs(p["t2"] - 110.85) < 1e-9
    assert p["stop"] < 100 < p["t1"] < p["t2"] and p["t1_r"] >= 1.5


def test_structure_plan_passes_when_no_room_or_stop_too_wide_or_no_support():
    assert "needs 1.5R of room" in L.structure_plan(A, 104.0, 1.5, True)["text"] or "too far" in L.structure_plan(A, 104.0, 1.5, True)["text"]
    near = {"ok": True, "zones": [Z(98, 98.8, "Moderate", "support"), Z(101.5, 102, "Strong", "resistance")]}
    r = L.structure_plan(near, 100.0, 1.5, True)
    assert not r["ok"] and "room" in r["fail"]
    assert not L.structure_plan(A, 100.0, 0.3, True)["ok"]                         # support 2R+ away vs a tiny ATR -> stop too wide
    assert "no support zone" in L.structure_plan({"ok": True, "zones": [Z(106, 107, "Strong", "resistance")]}, 100.0, 1.5, True)["fail"]
    assert not L.structure_plan(None, 100.0, 1.5, True)["ok"]


def test_structure_plan_ignores_weak_zones_and_clear_sky_defaults():
    weak = {"ok": True, "zones": [Z(98, 98.8, "Moderate", "support"), Z(103, 104, "Weak", "resistance")]}
    p = L.structure_plan(weak, 100.0, 1.5, True)
    assert p["ok"] and abs(p["t1_r"] - 1.5) < 1e-9 and abs(p["t2_r"] - 3.0) < 1e-9


def test_structure_plan_short_mirrors():
    a = {"ok": True, "zones": [Z(101.2, 102, "Strong", "resistance"), Z(94, 95, "Strong", "support"), Z(90, 91, "Moderate", "support")]}
    p = L.structure_plan(a, 100.0, 1.5, False)
    assert p["ok"] and p["stop"] > 100 > p["t1"] > p["t2"]


def test_trend_break_warning_only_for_matching_direction():
    a = {"ok": True, "timeframes": [{"label": "Intermediate", "tf": "1h", "direction": "UP", "state": "broken", "invalidation": 95.0},
                                    {"label": "Minor", "tf": "15m", "direction": "UP", "state": "broken", "invalidation": 99.0}]}
    assert "1h uptrend structure just broke" in L.trend_break_warning(a, long=True)
    assert L.trend_break_warning(a, long=False) == "" and L.trend_break_warning(None) == ""
    a["timeframes"][0]["state"] = "intact"
    assert L.trend_break_warning(a, long=True) == ""            # the minor scale alone does not trigger it


def test_engine_at_matches_truncated_history():
    b = make_bars(120, seed=9, price=2500)
    eng = L.Engine(b, L.CRYPTO_TFS)
    for cut in (288 * 60, 288 * 90 + 41):
        t = b.index[cut - 1] + pd.Timedelta(minutes=5)
        x, y = eng.at(t, full=False), L.analyze(b.iloc[:cut])
        assert [(round(z["low"], 6), round(z["high"], 6), z["strength"]) for z in x["zones"]] == [(round(z["low"], 6), round(z["high"], 6), z["strength"]) for z in y["zones"]]
        assert x["alignment"] == y["alignment"]


def test_prior_day_levels_are_last_complete_day():
    b = make_bars(30, seed=2)
    eng = L.Engine(b, L.CRYPTO_TFS)
    t = b.index[288 * 20 + 100] + pd.Timedelta(minutes=5)           # mid-day on the 21st day (index 20)
    tt = np.datetime64(t.tz_convert("UTC").tz_localize(None), "ns")
    kd = int(np.searchsorted(eng.d_av, tt, side="right"))
    assert kd == 20                                                  # days 0..19 are complete; day 20 is still forming
    assert eng.daily.index[kd - 1] == b.index[0].normalize() + pd.Timedelta(days=19)     # "prior day" = yesterday
    a = eng.at(t, full=False)
    y = eng.daily.iloc[kd - 1]
    hit = [z for z in a["zones"] if "prior day high" in z["labels"]]
    assert not hit or any(z["low"] <= y.high <= z["high"] for z in hit)


def _data(days=200, seed=7):
    b = make_bars(days, seed=seed)
    r = make_bars(days, seed=seed + 50, price=60000)
    return b, add_features(resample_bars(b, 15), resample_bars(r, 15), tf=15)


def test_simulate_chart_mode_passes_trades_and_prices_exits_from_zones():
    b, d = _data()
    eng = L.Engine(b, L.CRYPTO_TFS)
    s = Settings()
    skips = []
    atr_t = simulate(d, REGISTRY["trend_pullback"](), s, "ETH-USD")
    ch_t = simulate(d, REGISTRY["trend_pullback"](), s, "ETH-USD", engine=eng, exit_mode="chart", skips=skips)
    assert len(skips) > 0 and len(atr_t) > 0
    assert all(r["reason"] for r in skips)
    assert (ch_t.risk > 0).all()


def test_compare_exits_is_paired_and_reports_skips():
    b, d = _data()
    s = Settings()
    ce = compare_exits(d, s, "ETH-USD", list(s.enabled_strategies), L.Engine(b, L.CRYPTO_TFS))
    assert ce["verdict"] in ("INSUFFICIENT_SAMPLE", "CHART_EXITS_BETTER", "CHART_EXITS_WORSE", "NOT_DEMONSTRATED")
    tp = ce["per_strategy"]["trend_pullback"]["all_sample"]
    assert tp["trades"] == tp["with_chart_plan"] + tp["skipped_no_clean_plan"]
    assert set(tp["skip_reasons"]) <= {"no room before resistance", "stop would be too wide", "no support zone for a stop", "chart analysis unavailable"}


def test_run_research_includes_chart_exit_section_only_with_engine():
    b, d = _data(150)
    s = Settings()
    assert run_research(d, s, "ETH-USD")["chart_exits"] is None
    rep = run_research(d, s, "ETH-USD", engine=L.Engine(b, L.CRYPTO_TFS))
    assert rep["chart_exits"]["pooled_out_of_sample"] is not None


def test_scan_chart_mode_uses_zone_levels_or_reports_why_not():
    b, d = _data(150)
    eng = L.Engine(b, L.CRYPTO_TFS)
    fake = {"ok": True, "zones": [Z(float(d.close.iloc[-1]) * 0.9, float(d.close.iloc[-1]) * 0.92, "Strong", "support")]}
    for mode in ("atr", "chart"):
        s = Settings(exit_mode=mode)
        rows = scan(s, d, "ETH-USD", levels=fake)
        for r in rows:
            if r["status"] == "SIGNAL":
                assert r["plan_mode"] in ("atr", "chart", "chart_none")
                if mode == "chart":
                    assert r["plan_mode"] == "chart_none" and "No practice trade" in signal_text(r, s)


def test_gate_blocks_chart_none():
    s = Settings(exit_mode="chart")
    with tempfile.TemporaryDirectory() as t:
        led = CryptoLedger(s, Path(t), "ETH-USD")
        why = runner._gate(s, Path(t), led, [led], pd.Timestamp.now(tz="UTC"), False, {"blended_rr": 2.0, "plan_mode": "chart_none", "skip_reason": "no room"})
        assert "no clean chart-based plan" in why


def test_ledger_uses_chart_prices_and_cancels_gapped_entries():
    b, d = _data(30)
    s = Settings()
    i = len(d) - 40
    entry_px = float(d.open.iloc[i + 1])
    atr = float(d.atr.iloc[i])
    base_plan = {"strategy": "trend_pullback", "label": "x", "signal_time": str(d.index[i]), "atr": atr, "stop_atr": 1.5, "t1_r": 1.5, "t2_r": 3.0,
                 "max_hold_hours": 2.0, "units": 1.0, "regime": "x", "plan_mode": "chart"}
    with tempfile.TemporaryDirectory() as t:
        led = CryptoLedger(s, Path(t), "ETH-USD")
        led.open_position({**base_plan, "stop_price": entry_px - 3 * atr, "t1_price": entry_px + 5 * atr, "t2_price": entry_px + 9 * atr})
        ev = led.update(d, pd.Timestamp.now(tz="UTC"))
        cl = led.closed()
        assert len(cl) == 1 and abs(float(cl.risk_per_unit.iloc[0]) - 3 * atr) < 0.2 * atr    # risk comes from the chart stop (plus slippage)
    with tempfile.TemporaryDirectory() as t:
        led = CryptoLedger(s, Path(t), "ETH-USD")
        led.open_position({**base_plan, "signal_time": str(d.index[i - 1]), "stop_price": entry_px + 1.0, "t1_price": entry_px + 5 * atr, "t2_price": entry_px + 9 * atr})
        ev = led.update(d, pd.Timestamp.now(tz="UTC"))
        assert any(e["type"] == "ENTRY_CANCELLED" for e in ev) and led.positions() == [] and len(led.closed()) == 0


def test_exit_mode_setting_is_validated():
    import os
    from cryptoai.config import load_settings
    os.environ["CRYPTOAI_EXIT_MODE"] = "banana"
    try:
        try:
            load_settings()
            assert False
        except ValueError:
            pass
    finally:
        os.environ.pop("CRYPTOAI_EXIT_MODE")
    assert load_settings().exit_mode == "atr"


def test_present_lines():
    from cryptoai import present as P
    ok = L.structure_plan(A, 100.0, 1.5, True)
    assert "These levels come from the chart" in P.chart_plan_line({"chart_plan": ok, "plan_mode": "chart"}, "ETH-USD")
    assert "Chart-based alternative" in P.chart_plan_line({"chart_plan": ok, "plan_mode": "atr"}, "ETH-USD")
    bad = L.structure_plan(None, 100.0, 1.5, True)
    assert "would pass" in P.chart_plan_line({"chart_plan": bad, "plan_mode": "atr"}, "ETH-USD")
    assert "No practice trade" in P.chart_plan_line({"chart_plan": bad, "plan_mode": "chart_none", "skip_reason": "x"}, "ETH-USD")
    assert P.chart_plan_line({}, "ETH-USD") == ""


def test_evaluate_end_to_end_in_chart_mode():
    from tests.test_runner import _setup
    import os
    with tempfile.TemporaryDirectory() as t:
        base = Path(t)
        os.environ["CRYPTOAI_STATE_DIR"] = t
        for k in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"):
            os.environ.pop(k, None)
        _setup(base)
        s = Settings(exit_mode="chart", symbols=("ETH-USD", "AERO-USD"))
        assert runner.cmd_evaluate(s, base, fetch=False) == 0
        assert (base / "ETH-USD" / "levels.json").exists()
        for sym in s.symbols:
            for p in CryptoLedger(s, base, sym).positions():
                assert p["plan_mode"] == "chart" and p["stop_price"] < p["t1_price"] < p["t2_price"]
