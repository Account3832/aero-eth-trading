"""Settings and the global kill switch. Everything here is PAPER ONLY."""
from __future__ import annotations

import os
from dataclasses import dataclass, fields
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
BAR_MIN = 5
BARS_PER_DAY = 288


def state_dir() -> Path:
    """Where runtime state lives. In GitHub Actions this points at the `data` branch checkout."""
    p = Path(os.environ.get("CRYPTOAI_STATE_DIR", ROOT / "state"))
    p.mkdir(parents=True, exist_ok=True)
    return p


def now_utc() -> pd.Timestamp:
    return pd.Timestamp.now(tz="UTC")


@dataclass
class Settings:
    # instruments (spot pairs on Coinbase). BTC is read-only market context, never traded.
    symbols: tuple = ("ETH-USD", "AERO-USD")
    ref_symbol: str = "BTC-USD"
    # account assumptions (paper money, configurable)
    account_equity: float = 10000.0
    max_risk_pct: float = 0.5               # % of equity risked per trade
    max_daily_loss_pct: float = 2.0         # stop opening trades for the rest of the UTC day
    max_trades_per_day: int = 6             # per coin
    max_total_open: int = 2                 # across all coins (ETH and AERO move together, so keep this low)
    min_blended_rr: float = 1.5             # average of the two targets, in R, must be at least this
    # costs, % of trade value PER SIDE. These are assumptions: change them to your real fees.
    fee_pct: float = 0.10
    slip_pct_eth: float = 0.03
    slip_pct_aero: float = 0.10
    cooldown_min: int = 30                  # minutes to wait after a trade closes (per coin)
    # candle size for entries. 5-minute stores are resampled. Bigger candles = fewer trades and much less fee drag.
    entry_minutes: int = 15
    # data freshness (minutes, on top of one candle length)
    max_bar_slack_min: int = 15
    # research
    min_trades_for_claim: int = 100
    enabled_strategies: tuple = ("trend_pullback", "donchian_breakout", "squeeze_breakout", "oversold_bounce")
    # tested and reported, but never used for practice trades until they pass the fair test and are moved above
    research_only_strategies: tuple = ("range_bounce", "btc_lead", "support_bounce", "swing_breakout", "steady_scalper")
    notify_research_signals: bool = False
    exit_mode: str = "atr"            # "atr" = fixed ATR stop and R targets; "chart" = stop/targets from support and resistance zones
    struct_min_room_r: float = 1.5
    struct_min_risk_atr: float = 0.8
    struct_max_risk_atr: float = 3.0
    struct_buffer_atr: float = 0.25
    mode: str = "paper"                     # live execution does not exist in this code

    @property
    def bars_per_day(self) -> int:
        return 1440 // self.entry_minutes

    @property
    def bars_per_hour(self) -> int:
        return max(60 // self.entry_minutes, 1)

    @property
    def cooldown_bars(self) -> int:
        return -(-self.cooldown_min // self.entry_minutes)

    @property
    def max_bar_age_min(self) -> int:
        return self.entry_minutes + self.max_bar_slack_min

    def slip_pct(self, symbol: str) -> float:
        return self.slip_pct_aero if symbol.upper().startswith("AERO") else self.slip_pct_eth

    def struct_params(self) -> dict:
        return {"min_room_r": self.struct_min_room_r, "min_risk_atr": self.struct_min_risk_atr, "max_risk_atr": self.struct_max_risk_atr,
                "buffer_atr": self.struct_buffer_atr}

    def decimals(self, symbol: str) -> int:
        return 5 if symbol.upper().startswith("AERO") else 2

    @property
    def risk_usd(self) -> float:
        return self.account_equity * self.max_risk_pct / 100.0


def load_settings(path: str | os.PathLike | None = None) -> Settings:
    s = Settings()
    p = Path(path) if path else ROOT / "config" / "settings.yaml"
    if p.exists():
        import yaml
        data = yaml.safe_load(p.read_text()) or {}
        names = {f.name for f in fields(Settings)}
        for k, v in data.items():
            if k in names:
                setattr(s, k, tuple(v) if isinstance(v, list) else v)
    for f in fields(Settings):  # env overrides: CRYPTOAI_<NAME>
        raw = os.environ.get("CRYPTOAI_" + f.name.upper())
        if raw is not None:
            cur = getattr(s, f.name)
            if isinstance(cur, bool):
                setattr(s, f.name, raw.lower() in ("1", "true", "yes"))
            elif isinstance(cur, int):
                setattr(s, f.name, int(raw))
            elif isinstance(cur, float):
                setattr(s, f.name, float(raw))
            elif isinstance(cur, str):
                setattr(s, f.name, raw)
    if s.exit_mode not in ("atr", "chart"):
        raise ValueError("exit_mode must be 'atr' or 'chart'.")
    if s.mode != "paper":
        raise ValueError("Only mode='paper' is supported. Live execution is intentionally not implemented.")
    return s


def kill_switch(state: Path | None = None) -> tuple[bool, str]:
    """Global pause: env var CRYPTOAI_KILL, a KILL_SWITCH file, or control.json {"paused": true}."""
    if os.environ.get("CRYPTOAI_KILL", "").lower() in ("1", "true", "yes"):
        return True, "CRYPTOAI_KILL environment variable is set"
    sd = state or state_dir()
    if (sd / "KILL_SWITCH").exists():
        return True, "KILL_SWITCH file exists"
    ctl = sd / "control.json"
    if ctl.exists():
        import json
        try:
            if json.loads(ctl.read_text()).get("paused"):
                return True, "control.json paused=true"
        except Exception:
            return True, "control.json unreadable, failing safe"
    return False, ""
