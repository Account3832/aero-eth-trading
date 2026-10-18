"""Live monitor: checks EVERY strategy (practice and research-only) against the newest completed candle.

Used by the dashboard and by the 5-minute scheduled job. A "signal" is a rule firing on the latest candle,
never an order. Long-only: spot coins cannot be shorted.
"""
from __future__ import annotations

import math

import pandas as pd

from .config import Settings
from .levels import room_to_levels, structure_plan
from .paper import size_position
from .strategies import BASELINE, REGISTRY

STATUS_ORDER = {"SIGNAL": 0, "FORMING": 1, "WAITING": 2, "OFF": 3}


def _num(x):
    try:
        v = float(x)
        return None if math.isnan(v) else v
    except (TypeError, ValueError):
        return None


def scan(s: Settings, feats: pd.DataFrame, symbol: str, names=None, levels: dict | None = None) -> list[dict]:
    """One row per strategy for the LAST completed candle of `feats` (output of add_features)."""
    if feats is None or len(feats) < 50:
        return []
    live = set(s.enabled_strategies)
    names = list(names or (*s.enabled_strategies, *s.research_only_strategies))
    last = feats.iloc[-1]
    atr = _num(last.atr)
    bar_close = feats.index[-1] + pd.Timedelta(minutes=s.entry_minutes)
    dp = s.decimals(symbol)
    rows = []
    for n in names:
        if n not in REGISTRY:
            continue
        inst = REGISTRY[n]()
        kind = "Live practice" if n in live else ("Comparison" if n == "steady_scalper" else "Research only")
        row = {"symbol": symbol, "strategy": n, "kind": kind, "status": "WAITING", "trigger": "", "entry_ref": None, "stop": None,
               "target1": None, "target2": None, "risk_per_unit": None, "units": None, "notional_usd": None, "risk_usd": None,
               "blended_rr": inst.blended_rr, "atr": atr, "stop_atr": inst.stop_atr, "t1_r": inst.t1_r, "t2_r": inst.t2_r,
               "max_hold_hours": inst.max_hold_hours, "regime": str(last.regime), "note": "", "bar_close": str(bar_close),
               "waiting_for": inst.spec.trigger}
        try:
            sig = inst.signals(feats).iloc[-1]
        except Exception as e:  # noqa: BLE001
            row.update(status="OFF", note=f"could not be checked: {type(e).__name__}")
            rows.append(row)
            continue
        if int(sig["dir"]) == 1 and atr:
            risk = inst.stop_atr * atr
            entry = float(last.close)
            size = size_position(s, symbol, entry, risk)
            row.update(status="SIGNAL", trigger=str(sig["trigger"]), entry_ref=round(entry, dp), risk_per_unit=round(risk, dp + 1),
                       stop=round(entry - risk, dp), target1=round(entry + inst.t1_r * risk, dp), target2=round(entry + inst.t2_r * risk, dp),
                       units=size["units"], notional_usd=size["notional_usd"], risk_usd=size["risk_usd"],
                       note="The rule fired on the newest completed candle. Entry would be the NEXT candle's open.")
            cp = structure_plan(levels, entry, atr, True, **s.struct_params())
            row["chart_plan"] = {k: (round(v, dp + 1) if isinstance(v, float) else v) for k, v in cp.items()}
            row["plan_mode"] = "atr"
            if s.exit_mode == "chart":
                if cp["ok"]:
                    size = size_position(s, symbol, entry, cp["risk"])
                    row.update(plan_mode="chart", stop=round(cp["stop"], dp), target1=round(cp["t1"], dp), target2=round(cp["t2"], dp),
                               risk_per_unit=round(cp["risk"], dp + 1), blended_rr=cp["blended_rr"], units=size["units"],
                               notional_usd=size["notional_usd"], risk_usd=size["risk_usd"])
                else:
                    row.update(plan_mode="chart_none", skip_reason=cp["fail"])
            room = room_to_levels(levels, entry, row["risk_per_unit"], row["target1"], row["target2"], long=True)
            row["room"] = room
            if room.get("known") and row["plan_mode"] == "atr":
                row["note"] += " " + room["text"]
        else:
            try:
                blk = inst.blockers(feats)
            except Exception:  # noqa: BLE001
                blk = []
            if blk:
                row.update(status="FORMING", note="The trigger candle appeared, but " + "; ".join(blk) + ".")
            else:
                row["note"] = "Nothing close to triggering."
        rows.append(row)
    rows.sort(key=lambda r: (STATUS_ORDER[r["status"]], r["kind"] != "Live practice", r["strategy"]))
    return rows


def _chart_lines(r: dict, s: Settings) -> str:
    cp = r.get("chart_plan")
    if not cp:
        return ""
    if r.get("plan_mode") == "chart":
        return f"\nThese levels come from the chart: {cp['stop_basis']} for the stop, targets {cp['t1_basis']} and {cp['t2_basis']}."
    if r.get("plan_mode") == "chart_none":
        return f"\nChart-based exits are ON, but there is no clean plan: {r['skip_reason']}. No practice trade."
    if cp.get("ok"):
        return f"\nChart-based alternative: stop ${cp['stop']}, target 1 ${cp['t1']}, target 2 ${cp['t2']} ({cp['t1_basis']}; stop {cp['stop_basis']})."
    return f"\nChart-based exits would pass on this one: {cp['fail']}."


def signal_text(r: dict, s: Settings) -> str:
    coin = r["symbol"].split("-")[0]
    return (f"BUY {coin}: {r['strategy']} just signalled ({r['kind'].lower()}).\n"
            f"Entry: the next {s.entry_minutes}-minute candle open (about ${r['entry_ref']}).\n"
            f"Stop (exit if wrong): ${r['stop']}\n"
            f"Target 1: ${r['target1']} (sell half, then move the stop to entry)\n"
            f"Target 2: ${r['target2']} (sell the rest)\n"
            f"Size: about {r['units']} {coin} (${r['notional_usd']:,.0f}), risking about ${r['risk_usd']:.0f}.\n"
            f"If neither target is hit, get out after about {r['max_hold_hours']:g} hours."
            + (f"\nChart check: {r['room']['text']}" if (r.get("room") or {}).get("known") and r.get("plan_mode") == "atr" else "")
            + _chart_lines(r, s))
