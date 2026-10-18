import tempfile
from pathlib import Path

import pandas as pd

from cryptoai.data import ingest, parse_coinbase, parse_kraken, load_bars


def _cb_rows(start, n):
    t0 = int(pd.Timestamp(start, tz="UTC").timestamp())
    return [[t0 + 300 * i, 99.0, 101.0, 100.0, 100.5, 5.0] for i in range(n)][::-1]     # newest first, like Coinbase


def test_parse_coinbase_column_order():
    df = parse_coinbase(_cb_rows("2026-01-01", 3))
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert df.index.is_monotonic_increasing
    assert df.iloc[0].open == 100.0 and df.iloc[0].low == 99.0 and df.iloc[0].high == 101.0


def test_parse_kraken_column_order():
    t0 = int(pd.Timestamp("2026-01-01", tz="UTC").timestamp())
    df = parse_kraken([[t0, "10", "12", "9", "11", "10.5", "3", 4]])
    assert df.iloc[0].open == 10 and df.iloc[0].high == 12 and df.iloc[0].low == 9 and df.iloc[0].close == 11


def test_ingest_with_mock_server_ignores_out_of_window_rows():
    now = pd.Timestamp("2026-01-03 00:00", tz="UTC")

    def fake_get(url, params=None, **kw):
        a = pd.Timestamp(params["start"]); b = pd.Timestamp(params["end"])
        n = int((b - a).total_seconds() // 300) + 1
        rows = _cb_rows(a.tz_localize(None).isoformat() if a.tzinfo is None else a.tz_convert(None).isoformat(), n + 5)   # server returns extra rows
        return rows

    with tempfile.TemporaryDirectory() as t:
        r = ingest("ETH-USD", 2, now=now, base=Path(t), get=fake_get, sleep=lambda *_: None, log=lambda *_: None)
        assert r["ok"] and r["bars"] > 500
        b = load_bars("ETH-USD", Path(t), now)
        assert b.index.max() < now and b.index.is_monotonic_increasing and not b.index.duplicated().any()
        again = ingest("ETH-USD", 2, now=now, base=Path(t), get=fake_get, sleep=lambda *_: None, log=lambda *_: None)
        assert again["added"] == 0
