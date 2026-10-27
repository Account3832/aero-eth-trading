import json

import numpy as np
import pandas as pd

from cryptoai import levels as L
from tests.synth import make_bars


def zigzag(n_swings=12, leg=12, start=100.0, step=2.0, drift=1.0, tf="15min"):
    """Deterministic zig-zag: each leg moves up `step`+drift or down `step`, so highs and lows both rise (drift>0) or fall (drift<0)."""
    pts, p = [start], start
    for i in range(n_swings):
        p += (step + drift) if i % 2 == 0 else -step
        pts.append(p)
    close = np.concatenate([np.linspace(pts[i], pts[i + 1], leg, endpoint=False) for i in range(len(pts) - 1)])
    idx = pd.date_range("2026-01-01", periods=len(close), freq=tf, tz="UTC")
    return pd.DataFrame({"open": close, "high": close + 0.05, "low": close - 0.05, "close": close, "volume": 1.0}, index=idx)


def test_pivots_are_confirmed_after_the_fact():
    d = zigzag()
    p = L.pivots(d, 3, 3)
    assert len(p) >= 6
    assert ((p.cpos - p.pos) == 3).all() and p.cpos.max() < len(d)
    assert set(p.kind) == {"H", "L"}


def test_structure_up_and_down():
    up = L.structure(L.pivots(zigzag(drift=1.0), 3, 3), 110.0, 1.0)
    dn = L.structure(L.pivots(zigzag(drift=-1.0), 3, 3), 90.0, 1.0)
    assert up["direction"] == "UP" and up["state"] == "intact" and up["invalidation"] == up["swing_low"]
    assert dn["direction"] == "DOWN"


def test_structure_marks_break():
    p = L.pivots(zigzag(drift=1.0), 3, 3)
    s = L.structure(p, close=50.0, atr_now=1.0)          # far below the last higher low
    assert s["direction"] == "UP" and s["state"] == "broken"


def test_add_structure_is_causal():
    d = make_bars(40)
    full = L.add_structure(L.resample_tf(d, 15).copy(), 4, 4)
    part = L.add_structure(L.resample_tf(d.iloc[: 288 * 25], 15).copy(), 4, 4)
    cols = ["sw_hi", "sw_hi_prev", "sw_lo", "sw_lo_prev", "sw_trend"]
    common = part.index[-300:]
    assert np.allclose(full.loc[common, cols].fillna(-1).values, part.loc[common, cols].fillna(-1).values)


def test_add_structure_values_on_zigzag():
    d = L.add_structure(zigzag(drift=1.0).copy(), 3, 3)
    assert d.sw_trend.iloc[-1] == 1 and d.sw_hi.iloc[-1] > d.sw_hi_prev.iloc[-1] and d.sw_lo.iloc[-1] > d.sw_lo_prev.iloc[-1]


def test_resample_drops_the_still_forming_candle():
    d = make_bars(3)
    cut = d.iloc[: 288 * 2 + 5]           # ends 00:20 on day 3 -> the 1h candle starting 00:00 is not finished
    h = L.resample_tf(cut, 60)
    assert h.index[-1] + pd.Timedelta(hours=1) <= cut.index[-1] + pd.Timedelta(minutes=5)
    dd = L.resample_tf(cut, "D")
    assert dd.index[-1] + pd.Timedelta(days=1) <= cut.index[-1] + pd.Timedelta(minutes=5)


def test_alignment_cases():
    def row(label, w, direction, state="intact"):
        return {"label": label, "weight": w, "direction": direction, "state": state}
    a = L.alignment([row("Primary", 3, "UP"), row("Secondary", 2, "UP"), row("Intermediate", 1.5, "DOWN"), row("Minor", 1, "DOWN")])
    assert a["kind"] == "PULLBACK_IN_UPTREND"
    b = L.alignment([row(x, 1, "UP") for x in ("Primary", "Secondary", "Intermediate", "Minor")])
    assert b["kind"] == "ALIGNED_UP" and b["score"] == 1.0
    c = L.alignment([row("Primary", 3, "DOWN"), row("Secondary", 2, "DOWN"), row("Intermediate", 1.5, "UP"), row("Minor", 1, "UP")])
    assert c["kind"] == "BOUNCE_IN_DOWNTREND"
    broken = L.alignment([row("Primary", 3, "UP", "broken"), row("Secondary", 2, "UP", "broken")])
    assert broken["bias"] == "NEUTRAL"


def test_zones_cluster_and_roles():
    now = pd.Timestamp("2026-01-10", tz="UTC")
    pts = [{"price": p, "kind": k, "w": 1.0, "time": now - pd.Timedelta(days=2), "tf": "1h", "label": "Intermediate"}
           for p, k in ((100.0, "L"), (100.2, "L"), (100.1, "H"), (110.0, "H"), (110.1, "H"))]
    z = L.build_zones(pts, price=105.0, tol=0.5, atr_ref=1.0, now=now)
    roles = sorted((round(x["mid"]), x["role"], x["touches"]) for x in z)
    assert roles == [(100, "support", 3), (110, "resistance", 2)]


def test_role_reversal_needs_two_touches():
    now = pd.Timestamp("2026-01-10", tz="UTC")
    mk = lambda p, k: {"price": p, "kind": k, "w": 1.0, "time": now, "tf": "1h", "label": "x"}
    z = L.build_zones([mk(100.0, "H"), mk(100.1, "H")], price=105.0, tol=0.5, atr_ref=1.0, now=now)
    assert z[0]["role"] == "support" and "role reversal" in (z[0]["former"] or "")
    z1 = L.build_zones([mk(100.0, "H")], price=105.0, tol=0.5, atr_ref=1.0, now=now)
    assert z1[0]["former"] is None


def test_room_to_levels_blocks_target():
    a = {"ok": True, "zones": [{"low": 103.0, "high": 103.5, "mid": 103.2, "strength": "Strong", "touches": 4, "role": "resistance"}]}
    r = L.room_to_levels(a, entry=100.0, risk=2.0, t1=104.0, t2=108.0, long=True)
    assert r["blocks_t1"] is True and r["dist_r"] == 1.5 and "BEFORE target 1" in r["text"]
    weak = {"ok": True, "zones": [{**a["zones"][0], "strength": "Weak"}]}
    assert L.room_to_levels(weak, 100.0, 2.0, 104.0, 108.0)["blocks_t1"] is False
    assert L.room_to_levels(None, 100.0, 2.0, 103.0, 106.0)["known"] is False


def test_analyze_end_to_end_and_json():
    a = L.analyze(make_bars(300, seed=5, price=2500), L.CRYPTO_TFS)
    assert a["ok"] and len(a["timeframes"]) == 5 and a["zones"]
    json.dumps(a)
    sup = a["nearest_support"]; res = a["nearest_resistance"]
    if sup:
        assert sup["mid"] < a["price"]
    if res:
        assert res["mid"] > a["price"]
    assert L.analyze(make_bars(1).iloc[:100], L.CRYPTO_TFS)["ok"] is False


def test_signal_text_includes_chart_check_when_known():
    from cryptoai.monitor import signal_text
    from cryptoai.config import Settings
    r = {"symbol": "ETH-USD", "strategy": "support_bounce", "kind": "Research only", "entry_ref": 2500.0, "stop": 2450.0, "target1": 2575.0,
         "target2": 2650.0, "units": 1.0, "notional_usd": 2500.0, "risk_usd": 50.0, "max_hold_hours": 6.0, "plan_mode": "atr",
         "room": {"known": True, "text": "Next resistance zone: 2560 (strong), 1.2R from entry - BEFORE target 1."}}
    assert "Chart check: Next resistance zone" in signal_text(r, Settings())
    r["room"] = {"known": False, "text": ""}
    assert "Chart check" not in signal_text(r, Settings())
