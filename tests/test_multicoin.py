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
    assert s.family_tests() == 12 * 10
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


# ---------------------------------------------------------------- trader-style checklist and the 5-minute scale

def _chart(kind="PULLBACK_IN_UPTREND", zones=None):
    z = zones if zones is not None else [{"low": 98.0, "high": 99.0, "mid": 98.5, "strength": "Strong", "touches": 4, "role": "support"}]
    return {"ok": True, "alignment": {"kind": kind}, "zones": z}


def test_confluence_check_rules():
    from cryptoai.levels import confluence_check
    ok = confluence_check(_chart(), entry=100.0, atr=1.0, bar_low=98.9, bar_close=99.8)
    assert ok["ok"] and ok["zone"]["mid"] == 98.5
    assert not confluence_check(_chart("ALIGNED_DOWN"), 100.0, 1.0, 98.9, 99.8)["ok"]                     # bigger trend down
    assert not confluence_check(_chart(zones=[{"low": 98, "high": 99, "mid": 98.5, "strength": "Moderate", "touches": 2, "role": "support"}]),
                                100.0, 1.0, 98.9, 99.8)["ok"]                                              # zone not strong
    assert not confluence_check(_chart(), 100.0, 1.0, 101.5, 102.0)["ok"]                                  # candle never reached the zone
    assert not confluence_check(_chart(), 103.0, 1.0, 98.9, 99.8)["ok"]                                    # entry far above the zone: too late
    assert not confluence_check(None, 100.0, 1.0, 98.9, 99.8)["ok"]
    res = [{"low": 101.0, "high": 102.0, "mid": 101.5, "strength": "Strong", "touches": 4, "role": "resistance"}]
    short = confluence_check(_chart("BOUNCE_IN_DOWNTREND", res), entry=100.0, atr=1.0, bar_low=99.5, bar_close=100.4, bar_high=101.2, long=False)
    assert short["ok"] and short["zone"]["mid"] == 101.5
    assert not confluence_check(_chart("ALIGNED_UP", res), 100.0, 1.0, 99.5, 100.4, bar_high=101.2, long=False)["ok"]   # bigger trend up: no short
    assert not confluence_check(_chart("ALIGNED_DOWN", res), 100.0, 1.0, 99.5, 100.4, bar_high=99.0, long=False)["ok"]    # never reached the zone


def test_five_minute_scale_reads_trend_only():
    from cryptoai.levels import CRYPTO_TFS, Engine
    assert CRYPTO_TFS[-1][:2] == ("Micro", 5)
    df = make_bars(120, start=(pd.Timestamp.now(tz="UTC").floor("D") - pd.Timedelta(days=120)).strftime("%Y-%m-%d"), seed=5, price=100)
    a = Engine(df, CRYPTO_TFS).at(df.index[-1] + pd.Timedelta(minutes=5))
    labels = [r["label"] for r in a["timeframes"]]
    assert labels == ["Primary", "Secondary", "Intermediate", "Minor", "Micro"]
    assert all("Micro" not in (z.get("labels") or []) for z in a["zones"])    # its swings never become zones


def test_zone_rejection_needs_the_chart_engine_and_is_research_only():
    from cryptoai.backtest import simulate
    from cryptoai.levels import CRYPTO_TFS, Engine
    from cryptoai.data import load_bars
    from cryptoai.strategies import REGISTRY
    assert "zone_rejection" in Settings().research_only_strategies and "zone_rejection" not in Settings().enabled_strategies
    with tempfile.TemporaryDirectory() as t:
        base = Path(t)
        _bars_for(base, ["ETH-USD", "BTC-USD"], 200)
        s = Settings(symbols=("ETH-USD",))
        d = runner.prepare(s, "ETH-USD", base)
        strat = REGISTRY["zone_rejection"]()
        assert len(simulate(d, strat, s, "ETH-USD")) == 0                 # no engine -> not testable, never silently runs on ATR exits
        skips = []
        tr = simulate(d, strat, s, "ETH-USD", engine=Engine(load_bars("ETH-USD", base), CRYPTO_TFS), skips=skips)
        assert len(tr) + len(skips) > 0                                   # candidates were found and each was either traded or explained
        for r in tr.itertuples():
            assert r.risk > 0 and r.exit_reason


def test_zone_rejection_not_proven_never_trades_live():
    with tempfile.TemporaryDirectory() as t:
        base = Path(t)
        _bars_for(base, ["ETH-USD", "BTC-USD"], 120)
        s = Settings(symbols=("ETH-USD",))
        d = runner.prepare(s, "ETH-USD", base)
        rows = scan(s, d, "ETH-USD", proven=set())
        z = [r for r in rows if r["strategy"] == "zone_rejection"]
        assert len(z) == 1 and z[0]["kind"] != "Live practice"
