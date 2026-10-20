"""Paper-trading ledger for one coin. Simulated fills only; nothing here talks to an exchange.

Positions are re-resolved from the stored bars on every update using the SAME conservative rules as the backtester
(resolve_trade), so the process is idempotent and restart-safe.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

from .backtest import resolve_trade
from .config import Settings, unit_decimals
from .store import read_json, write_json

CLOSED_COLS = ["id", "symbol", "strategy", "label", "signal_time", "entry_time", "exit_time", "entry", "risk_per_unit", "units",
               "notional_usd", "net_R", "gross_R", "pnl_usd", "exit_reason", "regime", "evidence_status"]


def trade_id(label: str, symbol: str, signal_ts) -> str:
    return hashlib.sha1(f"{label}|{symbol}|{pd.Timestamp(signal_ts).isoformat()}".encode()).hexdigest()[:12]


def size_position(s: Settings, symbol: str, entry: float, risk_per_unit: float) -> dict:
    """Units so a stop-out loses about the risk budget, capped so the position never exceeds the account (no leverage)."""
    if not (entry > 0 and risk_per_unit > 0):
        return {"units": 0.0, "notional_usd": 0.0, "risk_usd": 0.0, "capped": False}
    want = s.risk_usd / risk_per_unit
    cap = s.account_equity * 0.95 / entry
    units = min(want, cap)
    dec = unit_decimals(symbol)
    units = round(units, dec)
    return {"units": units, "notional_usd": round(units * entry, 2), "risk_usd": round(units * risk_per_unit, 2), "capped": want > cap}


class CryptoLedger:
    def __init__(self, s: Settings, base: Path, symbol: str):
        self.s, self.symbol = s, symbol
        self.dir = Path(base) / symbol
        self.dir.mkdir(parents=True, exist_ok=True)
        self.open_path, self.closed_path = self.dir / "open_positions.json", self.dir / "paper_trades.csv"

    def positions(self) -> list[dict]:
        return read_json(self.open_path, [])

    def closed(self) -> pd.DataFrame:
        if not self.closed_path.exists():
            return pd.DataFrame(columns=CLOSED_COLS)
        return pd.read_csv(self.closed_path)

    def open_position(self, plan: dict) -> bool:
        """Register a paper position. Idempotent on (strategy label, coin, signal bar)."""
        tid = trade_id(plan["label"], self.symbol, plan["signal_time"])
        if any(p["id"] == tid for p in self.positions()) or (len(self.closed()) and tid in set(self.closed()["id"])):
            return False
        write_json(self.open_path, self.positions() + [{**plan, "id": tid, "symbol": self.symbol, "created": str(pd.Timestamp.now(tz="UTC")),
                                                         "t1_alerted": False, "filled_alerted": False}])
        return True

    def update(self, feats: pd.DataFrame, now: pd.Timestamp) -> list[dict]:
        """feats: feature frame of COMPLETED bars. Returns events to alert on."""
        events, keep = [], []
        o, h, l, c = (feats[x].values for x in ("open", "high", "low", "close"))
        idx = feats.index
        slip_f, fee_f = self.s.slip_pct(self.symbol) / 100.0, self.s.fee_pct / 100.0
        for p in self.positions():
            sig_ts = pd.Timestamp(p["signal_time"])
            if sig_ts not in idx:
                keep.append(p)
                continue
            i = idx.get_loc(sig_ts)
            if i + 1 >= len(feats):          # entry candle has not completed yet
                keep.append(p)
                continue
            e_ref = o[i + 1]
            slip = slip_f * e_ref
            entry = e_ref + slip
            risk = p["stop_atr"] * p["atr"]
            stop, t1, t2 = entry - risk, entry + p["t1_r"] * risk, entry + p["t2_r"] * risk
            if p.get("plan_mode") == "chart":                  # stop and targets come from the chart, fixed at signal time
                stop, t1, t2 = float(p["stop_price"]), float(p["t1_price"]), float(p["t2_price"])
                risk = entry - stop
                if risk <= 0.2 * p["atr"] or t1 <= entry:      # price gapped past the plan before the fill
                    events.append({"type": "ENTRY_CANCELLED", "id": p["id"], "label": p["label"],
                                   "why": "Price opened beyond the chart-based plan, so there was no sensible entry."})
                    continue
            max_hold = max(int(p["max_hold_hours"] * 60 / self.s.entry_minutes), 1)
            res = resolve_trade(o, h, l, c, i + 1, e_ref, entry, risk, stop, t1, t2, slip, max_hold, data_end_closes=False)
            dp = self.s.decimals(self.symbol)
            if not p.get("filled_alerted"):
                events.append({"type": "ENTRY_FILLED", "id": p["id"], "label": p["label"], "entry": round(entry, dp)})
                p["filled_alerted"] = True
            if res["reasons"].get(1) == "T1" and not p.get("t1_alerted"):
                events.append({"type": "TARGET_REACHED", "id": p["id"], "label": p["label"], "t1": round(t1, dp)})
                p["t1_alerted"] = True
            if not res["closed"]:
                keep.append(p)
                continue
            units = float(p["units"] or 0)
            net_px = res["net"] - 2 * fee_f * entry
            row = {"id": p["id"], "symbol": self.symbol, "strategy": p["strategy"], "label": p["label"], "signal_time": p["signal_time"],
                   "entry_time": str(idx[i + 1]), "exit_time": str(idx[res["last_j"]]), "entry": round(entry, dp),
                   "risk_per_unit": round(risk, dp + 1), "units": units, "notional_usd": round(units * entry, 2),
                   "net_R": round(net_px / risk, 3), "gross_R": round(res["gross"] / risk, 3), "pnl_usd": round(net_px * units, 2),
                   "exit_reason": f"{res['reasons'].get(1, '')}|{res['reasons'].get(2, '')}", "regime": p.get("regime"),
                   "evidence_status": p.get("evidence_status", "")}
            self._append_closed(row)
            why = row["exit_reason"]
            kind = "STOP" if ("stop" in why and "BE" not in why) else ("TIME" if "maxhold" in why else "TARGET")
            events.append({"type": "EXIT_" + kind, "id": p["id"], "label": p["label"], "pnl_usd": row["pnl_usd"], "net_R": row["net_R"],
                           "reason": why, "exit_time": row["exit_time"]})
        write_json(self.open_path, keep)
        return events

    def _append_closed(self, row: dict):
        df = pd.concat([self.closed(), pd.DataFrame([row])], ignore_index=True)
        df = df.drop_duplicates(subset="id", keep="last")
        tmp = self.closed_path.with_suffix(".tmp")
        df.to_csv(tmp, index=False)
        tmp.replace(self.closed_path)

    def summary(self, now: pd.Timestamp) -> dict:
        today = now.date().isoformat()
        cl = self.closed()
        today_cl = cl[cl["exit_time"].astype(str).str[:10] == today] if len(cl) else cl
        opens = self.positions()
        opened_today = sum(1 for p in opens if str(p["signal_time"])[:10] == today)
        return {"trades_today": int(len(today_cl) + opened_today), "open_count": len(opens),
                "realized_today_usd": float(today_cl["pnl_usd"].sum()) if len(today_cl) else 0.0}
