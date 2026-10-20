import os
import tempfile
from pathlib import Path

import pandas as pd

from cryptoai import runner
from cryptoai.config import Settings
from cryptoai.monitor import scan, signal_text
from cryptoai.store import read_json, save_bars
from tests.synth import make_bars


def _setup(base: Path, days=200):
    end = pd.Timestamp.now(tz="UTC").floor("D")
    start = (end - pd.Timedelta(days=days)).strftime("%Y-%m-%d")
    for sym, seed, px in (("ETH-USD", 1, 2500), ("AERO-USD", 2, 1.2), ("BTC-USD", 3, 90000)):
        save_bars(sym, make_bars(days, start=start, seed=seed, price=px), base)


def test_backtest_and_evaluate_end_to_end():
    with tempfile.TemporaryDirectory() as t:
        base = Path(t)
        os.environ["CRYPTOAI_STATE_DIR"] = t
        for k in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"):
            os.environ.pop(k, None)
        _setup(base)
        s = Settings(symbols=("ETH-USD", "AERO-USD"))
        assert runner.cmd_backtest(s, base, 730) == 0
        for sym in s.symbols:
            assert (base / sym / "backtest_report.json").exists()
            assert (base / sym / "trade_log_2y.csv").exists()
        assert runner.cmd_evaluate(s, base, fetch=False) == 0
        st = read_json(base / "status.json")
        assert set(st["symbols"]) == {"ETH-USD", "AERO-USD"}
        assert (base / "ETH-USD" / "monitor.json").exists()


def test_scan_rows_have_levels_only_when_signal():
    with tempfile.TemporaryDirectory() as t:
        base = Path(t)
        _setup(base, 120)
        s = Settings()
        d = runner.prepare(s, "ETH-USD", base)
        rows = scan(s, d, "ETH-USD")
        assert {r["strategy"] for r in rows} >= set(s.enabled_strategies)
        for r in rows:
            assert r["status"] in ("SIGNAL", "FORMING", "WAITING", "OFF")
            if r["status"] == "SIGNAL":
                assert r["stop"] < r["entry_ref"] < r["target1"] < r["target2"]
                assert "BUY" in signal_text(r, s)
            else:
                assert r["stop"] is None


def test_kill_switch_blocks_new_trades():
    with tempfile.TemporaryDirectory() as t:
        base = Path(t)
        (base / "KILL_SWITCH").write_text("x")
        s = Settings()
        from cryptoai.paper import CryptoLedger
        led = CryptoLedger(s, base, "ETH-USD")
        row = {"blended_rr": 2.25}
        assert runner._gate(s, base, led, [led], pd.Timestamp.now(tz="UTC"), False, row).startswith("paused")


def test_telegram_not_configured_does_not_crash():
    for k in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"):
        os.environ.pop(k, None)
    from cryptoai.alerts import send_telegram
    assert send_telegram("hi") == "not_configured"
