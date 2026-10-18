"""Free, keyless 5-minute candles. Primary: Coinbase Exchange public API. Backup (latest ~60h only): Kraken public API.

Coinbase skips 5-minute slots when nothing traded, so stored bars are gap-filled on load (flat candle at the previous
close, volume 0). A candle is used only after it has CLOSED. No API key is needed and nothing is paid for.
"""
from __future__ import annotations

import time
from pathlib import Path

import pandas as pd

from .config import state_dir
from .store import COLS, load_raw, read_json, save_bars, write_json

CB_URL = "https://api.exchange.coinbase.com"
KRAKEN_URL = "https://api.kraken.com/0/public/OHLC"
KRAKEN_PAIR = {"ETH-USD": "ETHUSD", "AERO-USD": "AEROUSD", "BTC-USD": "XBTUSD"}
STEP = pd.Timedelta(minutes=5)
WINDOW_BARS = 300


class FeedError(Exception):
    pass


def _get(url: str, params: dict | None = None, retries: int = 4, sleep=time.sleep):
    import requests
    last = ""
    for k in range(retries):
        try:
            r = requests.get(url, params=params, timeout=20, headers={"User-Agent": "cryptoai-paper-research"})
            if r.status_code == 429 or r.status_code >= 500:
                last = f"http_{r.status_code}"
                sleep(1.5 * (k + 1))
                continue
            if not r.ok:
                raise FeedError(f"http_{r.status_code}: {r.text[:120]}")
            return r.json()
        except FeedError:
            raise
        except Exception as e:  # noqa: BLE001  network blip
            last = type(e).__name__
            sleep(1.5 * (k + 1))
    raise FeedError(f"gave up after {retries} tries ({last})")


def _frame(rows: list, order: list[str]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame(columns=COLS, index=pd.DatetimeIndex([], tz="UTC"))
    df = pd.DataFrame(rows, columns=order[: len(rows[0])])
    df["time"] = pd.to_datetime(df["time"].astype("int64"), unit="s", utc=True)
    df = df.set_index("time").sort_index()
    for c in COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df[COLS].dropna(subset=["open", "high", "low", "close"])


def parse_coinbase(rows: list) -> pd.DataFrame:
    """Coinbase candle rows are [time, low, high, open, close, volume], newest first."""
    return _frame(rows, ["time", "low", "high", "open", "close", "volume"])


def parse_kraken(rows: list) -> pd.DataFrame:
    """Kraken rows are [time, open, high, low, close, vwap, volume, count]."""
    return _frame(rows, ["time", "open", "high", "low", "close", "vwap", "volume", "count"])


def fetch_coinbase(product: str, start: pd.Timestamp, end: pd.Timestamp, get=_get) -> pd.DataFrame:
    rows = get(f"{CB_URL}/products/{product}/candles",
               {"granularity": 300, "start": start.strftime("%Y-%m-%dT%H:%M:%SZ"), "end": end.strftime("%Y-%m-%dT%H:%M:%SZ")})
    if not isinstance(rows, list):
        raise FeedError(f"unexpected Coinbase reply: {str(rows)[:120]}")
    df = parse_coinbase(rows)
    return df[(df.index >= start) & (df.index <= end)] if len(df) else df   # never trust the server to honor the window


def fetch_kraken(symbol: str, get=_get) -> pd.DataFrame:
    pair = KRAKEN_PAIR.get(symbol)
    if not pair:
        raise FeedError(f"no Kraken pair known for {symbol}")
    js = get(KRAKEN_URL, {"pair": pair, "interval": 5})
    if js.get("error"):
        raise FeedError("Kraken: " + ", ".join(js["error"])[:120])
    key = next(k for k in js["result"] if k != "last")
    return parse_kraken(js["result"][key])


def complete_only(df: pd.DataFrame, now: pd.Timestamp) -> pd.DataFrame:
    """Keep candles that have fully closed by `now`."""
    return df[df.index + STEP <= now] if len(df) else df


def fetch_recent(symbol: str, now: pd.Timestamp, get=_get) -> tuple[pd.DataFrame, str]:
    """About the last 25 hours of closed candles. Returns (frame, source name). Raises FeedError if both sources fail."""
    end = now.floor("5min")
    try:
        df = fetch_coinbase(symbol, end - (WINDOW_BARS - 1) * STEP, end, get)
        if len(df):
            return complete_only(df, now), "coinbase"
        err = "Coinbase returned no candles"
    except FeedError as e:
        err = str(e)
    try:
        return complete_only(fetch_kraken(symbol, get), now), "kraken (backup)"
    except FeedError as e2:
        raise FeedError(f"Coinbase: {err}; Kraken: {e2}") from None


def fill_gaps(df: pd.DataFrame) -> pd.DataFrame:
    """Full 5-minute grid. Missing slots become a flat candle at the previous close with zero volume."""
    if len(df) < 2:
        return df
    full = pd.date_range(df.index[0], df.index[-1], freq="5min", tz="UTC")
    out = df.reindex(full)
    out["close"] = out["close"].ffill()
    for c in ("open", "high", "low"):
        out[c] = out[c].fillna(out["close"])
    out["volume"] = out["volume"].fillna(0.0)
    return out


def resample_bars(df: pd.DataFrame, minutes: int) -> pd.DataFrame:
    """Aggregate gap-filled 5-minute bars into `minutes`-minute bars (index = bar start). Only COMPLETE bars are kept."""
    if minutes == 5 or len(df) == 0:
        return df
    rs = df.resample(f"{minutes}min", closed="left", label="left")
    out = rs.agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"})
    cnt = rs["close"].count()
    out = out[cnt == minutes // 5].dropna(subset=["close"])
    return out


def load_bars(symbol: str, base: Path | None = None, now: pd.Timestamp | None = None) -> pd.DataFrame:
    """Stored, closed, gap-filled bars (UTC index)."""
    df = load_raw(symbol, base)
    if now is not None:
        df = complete_only(df, now)
    return fill_gaps(df)


def gap_stats(symbol: str, base: Path | None = None) -> dict:
    raw = load_raw(symbol, base)
    if len(raw) < 2:
        return {"bars": len(raw), "missing": 0, "missing_pct": 0.0}
    full = len(pd.date_range(raw.index[0], raw.index[-1], freq="5min"))
    return {"bars": len(raw), "missing": full - len(raw), "missing_pct": round(100 * (full - len(raw)) / full, 2)}


def ingest(symbol: str, days: int, now: pd.Timestamp | None = None, base: Path | None = None, get=_get,
           sleep=time.sleep, log=print) -> dict:
    """Backfill and top up stored candles. Forward from the last stored bar; backward to now-days once per target."""
    base = base or state_dir()
    now = (now or pd.Timestamp.now(tz="UTC"))
    end_all = now.floor("5min")
    target = (end_all - pd.Timedelta(days=days)).floor("D")
    raw = load_raw(symbol, base)
    meta_path = base / "bars" / f"{symbol}_meta.json"
    meta = read_json(meta_path, {})
    spans = []
    if len(raw) == 0:
        spans.append((target, end_all))
    else:
        spans.append((raw.index[-1] + STEP, end_all))
        done_to = pd.Timestamp(meta["backfilled_to"]) if meta.get("backfilled_to") else None
        if raw.index[0] - target > pd.Timedelta(days=2) and (done_to is None or done_to > target):
            spans.append((target, raw.index[0] - STEP))
    added, errors, reqs = 0, [], 0
    for a, b in spans:
        cur = a
        while cur <= b:
            end = min(cur + (WINDOW_BARS - 1) * STEP, b)
            try:
                chunk = complete_only(fetch_coinbase(symbol, cur, end, get), now)
            except FeedError as e:
                errors.append(str(e))
                if len(errors) >= 3:
                    break
                sleep(2)
                continue
            reqs += 1
            if len(chunk):
                added += save_bars(symbol, chunk, base)["added"]
            cur = end + STEP
            sleep(0.12)
            if reqs % 100 == 0:
                log(f"  {symbol}: {reqs} requests, {added} new bars so far (at {cur})")
        if errors and len(errors) >= 3:
            break
    if not errors and len(spans) > 1:
        meta["backfilled_to"] = str(target)
        write_json(meta_path, meta)
    after = load_raw(symbol, base)
    return {"symbol": symbol, "ok": not errors, "added": added, "requests": reqs, "errors": errors[:3], "bars": len(after),
            "first": str(after.index[0]) if len(after) else None, "last": str(after.index[-1]) if len(after) else None,
            **gap_stats(symbol, base)}
