"""Read-only helpers the dashboard uses: load state from a local folder or from the repo's `data` branch URL."""
from __future__ import annotations

import io
import json
import os
from pathlib import Path

import pandas as pd

from .config import price_decimals


def _url() -> str:
    return os.environ.get("CRYPTOAI_STATE_URL", "").rstrip("/")


def read_text(rel: str, base: Path | None = None, timeout: int = 15) -> str | None:
    u = _url()
    try:
        if u:
            import requests
            r = requests.get(f"{u}/{rel}", timeout=timeout, headers={"Cache-Control": "no-cache"})
            return r.text if r.ok else None
        p = (base or Path(os.environ.get("CRYPTOAI_STATE_DIR", "state"))) / rel
        return p.read_text() if p.exists() else None
    except Exception:  # noqa: BLE001
        return None


def read_json_rel(rel: str, default=None, base: Path | None = None):
    t = read_text(rel, base)
    try:
        return json.loads(t) if t else default
    except Exception:  # noqa: BLE001
        return default


def read_csv_rel(rel: str, base: Path | None = None) -> pd.DataFrame:
    t = read_text(rel, base)
    if not t:
        return pd.DataFrame()
    try:
        return pd.read_csv(io.StringIO(t))
    except Exception:  # noqa: BLE001
        return pd.DataFrame()


def read_bars_rel(symbol: str, base: Path | None = None) -> pd.DataFrame:
    """Stored 5-minute bars (gzip CSV), local or remote."""
    import gzip
    rel = f"bars/{symbol}_5m.csv.gz"
    try:
        if _url():
            import requests
            r = requests.get(f"{_url()}/{rel}", timeout=60)
            raw = gzip.decompress(r.content) if r.ok else b""
        else:
            p = (base or Path(os.environ.get("CRYPTOAI_STATE_DIR", "state"))) / rel
            raw = gzip.decompress(p.read_bytes()) if p.exists() else b""
        if not raw:
            return pd.DataFrame()
        df = pd.read_csv(io.BytesIO(raw), index_col=0, parse_dates=True)
        df.index = pd.to_datetime(df.index, utc=True)
        return df
    except Exception:  # noqa: BLE001
        return pd.DataFrame()


def money(x, dp=2) -> str:
    try:
        return f"${float(x):,.{dp}f}"
    except (TypeError, ValueError):
        return "n/a"


def price(x, symbol: str) -> str:
    dp = price_decimals(symbol)
    return money(x, dp)


def verdict_plain(v: str) -> str:
    return {"NOT_DEMONSTRATED": "No proof it works", "INSUFFICIENT_SAMPLE": "Too few trades to judge", "FAILED_OOS": "Failed the fair test",
            "EDGE_SUPPORTED": "Passed the fair test (still not a promise)", "UNDERLYING_EDGE_SUPPORTED": "Passed the fair test (still not a promise)"}.get(v, v)


def exit_verdict_plain(v: str) -> str:
    return {"INSUFFICIENT_SAMPLE": "Too few trades to judge", "NOT_DEMONSTRATED": "No proof chart exits are better",
            "CHART_EXITS_BETTER": "Chart exits did better in the fair test (still not a promise)",
            "CHART_EXITS_WORSE": "Chart exits did worse in the fair test"}.get(v, v)


def chart_plan_line(r: dict, symbol: str) -> str:
    cp = r.get("chart_plan")
    if not cp:
        return ""
    if r.get("plan_mode") == "chart":
        return f"These levels come from the chart: stop {cp['stop_basis']}; target 1 {cp['t1_basis']}; target 2 {cp['t2_basis']}."
    if r.get("plan_mode") == "chart_none":
        return f"Chart-based exits are ON but there is no clean plan: {r['skip_reason']}. No practice trade."
    if cp.get("ok"):
        return (f"Chart-based alternative: stop {price(cp['stop'], symbol)}, target 1 {price(cp['t1'], symbol)}, target 2 {price(cp['t2'], symbol)} "
                f"({cp['t1_basis']}).")
    return f"Chart-based exits would pass on this one: {cp['fail']}."
