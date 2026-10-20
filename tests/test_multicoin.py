"""Many coins, the 'only alert on a pass' rule, the resumable download, and the keep-alive workflow."""
import os
import tempfile
import time
from pathlib import Path

import pandas as pd

from cryptoai import runner
from cryptoai.alerts import read_jsonl
from cryptoai.config import ROOT, Settings, price_decimals, unit_decimals
from cryptoai.data import ingest
from cryptoai.monitor import proven_strategies, scan
from cryptoai.paper import CryptoLedger
from cryptoai.store import save_bars, write_json
from tests.synth import make_bars


def _bars_for(base: Path, syms, days=150):
    end = pd.Timestamp.now(tz="UTC").floor("D")
    start = (end - pd.Timedelta(days=days)).strftime("%Y-%m-%d")
    for i, sym in enumerate(syms):
        save_bars(sym, make_bars(days, start=start, seed=10 + i, price=100 + i), base)


def test_default_coin_list_is_clean():
    s = Settings()
    assert len(s.symbols) == 12 and len(set(s.symbols)) == 12
    assert s.symbols[:2] == ("ETH-USD", "AERO-USD") and all(x.endswith("-USD") for x in s.symbols)
    assert s.family_tests() == 12 * 9
    for sym in s.symbols:
        assert 0 < s.slip_pct(sym) <= 0.10 and price_decimals(sym) >= 2 and unit_decimals(sym) >= 0
    assert s.slip_pct("UNKNOWN-USD") == 0.10   # cautious default for a coin we have no table entry for


def test_proven_strategies_reads_only_passes():
    rep = {"strategies": {"a": {"verdict": "EDGE_SUPPORTED"}, "b": {"verdict": "NOT_DEMONSTRATED"}, "c": {"verdict": "FAILED_OOS"},
                          "d": {"verdict": "INSUFFICIENT_SAMPLE"}, "e": {"verdict": "UNDERLYING_EDGE_SUPPORTED"}}}
    assert proven_strategies(rep) == {"a", "e"}
    assert proven_strategies({}) == set() and proven_strategies(None) == set()


def test_scan_labels_follow_proof():
    with tempfile.TemporaryDirectory() as t:
        base = Path(t)
        _bars_for(base, ["ETH-USD", "BTC-USD"], 120)
        s = Settings(symbols=("ETH-USD",))
        d = runner.prepare(s, "ETH-USD", base)
        none = scan(s, d, "ETH-USD", proven=set())
        assert none and all(r["kind"] != "Live practice" for r in none)
        one = scan(s, d, "ETH-USD", proven={"trend_pullback"})
        assert [r["strategy"] for r in one if r["kind"] == "Live practice"] == ["trend_pullback"]
        old = scan(Settings(symbols=("ETH-USD",), alert_only_proven=False), d, "ETH-USD")
        assert {r["strategy"] for r in old if r["kind"] == "Live practice"} == set(s.enabled_strategies)


def _fake_row(kind):
    return {"symbol": "ETH-USD", "strategy": "trend_pullback", "kind": kind, "status": "SIGNAL", "trigger": "x", "entry_ref": 100.0, "stop": 98.0,
            "target1": 103.0, "target2": 106.0, "risk_per_unit": 2.0, "units": 10.0, "notional_usd": 1000.0, "risk_usd": 20.0,
            "blended_rr": 2.5, "atr": 1.0, "stop_atr": 2.0, "t1_r": 1.5, "t2_r": 3.0, "max_hold_hours": 12, "regime": "trend",
            "note": "", "bar_close": "2026-01-01 00:00:00+00:00", "waiting_for": "x", "plan_mode": "atr"}


def test_unproven_signal_makes_no_trade_and_no_alert_but_proven_does():
    for kind, expect_trade in (("Not proven", 0), ("Live practice", 1)):
        with tempfile.TemporaryDirectory() as t:
            base = Path(t)
            os.environ["CRYPTOAI_STATE_DIR"] = t
            for k in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"):
                os.environ.pop(k, None)
            _bars_for(base, ["ETH-USD", "BTC-USD"], 120)
            s = Settings(symbols=("ETH-USD",), max_bar_slack_min=10 ** 7)
            real = runner.scan
            runner.scan = lambda *a, **k: [_fake_row(kind)]
            try:
                assert runner.cmd_evaluate(s, base, fetch=False) == 0
            finally:
                runner.scan = real
            assert len(CryptoLedger(s, base, "ETH-USD").positions()) == expect_trade
            kinds = [a["type"] for a in read_jsonl(base / "alerts.jsonl")] if (base / "alerts.jsonl").exists() else []
            assert ("ENTRY_TRIGGER_CONFIRMED" in kinds) == bool(expect_trade)
            assert "RESEARCH_SIGNAL" not in kinds   # unproven ideas are dashboard-only


def test_family_wide_bonferroni_makes_the_bar_stricter():
    from cryptoai.backtest import run_research
    with tempfile.TemporaryDirectory() as t:
        base = Path(t)
        _bars_for(base, ["ETH-USD", "BTC-USD"], 150)
        s = Settings(symbols=("ETH-USD",))
        d = runner.prepare(s, "ETH-USD", base)
        small = run_research(d, s, "ETH-USD", strategy_names=["trend_pullback"])
        big = run_research(d, s, "ETH-USD", strategy_names=["trend_pullback"], family_size=108)
        assert big["multiple_testing"]["family_size"] == 108
        assert big["multiple_testing"]["ci_level_used"] > small["multiple_testing"]["ci_level_used"] > 0.9
        assert big["multiple_testing"]["ci_level_used"] > 0.9995


def test_ingest_stops_at_deadline_and_resumes():
    calls = []

    def fake_get(url, params=None, **k):
        calls.append(params)
        start = pd.Timestamp(params["start"]).timestamp()
        return [[int(start + 300 * i), 1.0, 2.0, 1.5, 1.6, 10.0] for i in range(3)]
    with tempfile.TemporaryDirectory() as t:
        base = Path(t)
        now = pd.Timestamp("2026-06-10 12:00", tz="UTC")
        r = ingest("SOL-USD", 5, now=now, base=base, get=fake_get, sleep=lambda *_: None, log=lambda *_: None, deadline=time.monotonic() - 1)
        assert r["partial"] is True and r["requests"] == 0 and r["ok"] is True
        r2 = ingest("SOL-USD", 5, now=now, base=base, get=fake_get, sleep=lambda *_: None, log=lambda *_: None)
        assert r2["partial"] is False and r2["requests"] > 0


def test_unfinished_coins_are_skipped_by_the_five_minute_job():
    with tempfile.TemporaryDirectory() as t:
        base = Path(t)
        now = pd.Timestamp.now(tz="UTC")
        end = (now - pd.Timedelta(days=20)).floor("D")
        save_bars("SOL-USD", make_bars(60, start=(end - pd.Timedelta(days=60)).strftime("%Y-%m-%d"), seed=3), base)
        assert runner._still_loading("SOL-USD", base, now) is True
        assert runner._still_loading("NEVER-USD", base, now) is False   # nothing stored: the top-up fetches only 2 days


def test_keepalive_and_budgeted_research_workflows_exist():
    ka = (ROOT / ".github" / "workflows" / "keepalive.yml").read_text()
    assert "cron:" in ka and "gh workflow enable" in ka and "--allow-empty" in ka and "actions: write" in ka
    rs = (ROOT / ".github" / "workflows" / "research.yml").read_text()
    assert "--budget-min" in rs and "timeout-minutes: 90" in rs
