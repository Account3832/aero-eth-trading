"""Command line used by the scheduled jobs.   python -m cryptoai.runner <ingest|backtest|evaluate|telegram-test|status>

Runs 24/7 (crypto never closes). Paper only. Per-coin files live in <state>/<SYMBOL>/ .
"""
from __future__ import annotations

import argparse
import sys
import time

import pandas as pd

from .alerts import AlertType, find_chat_ids, send_alert, send_telegram, telegram_enabled, token_shape
from .backtest import report_markdown, run_research
from .config import kill_switch, load_settings, now_utc, state_dir
from .data import gap_stats, ingest, load_bars, resample_bars
from .store import load_raw
from .levels import CRYPTO_TFS, Engine, analyze, trend_break_warning
from .features import add_features
from .monitor import proven_strategies, scan, signal_text
from .paper import CryptoLedger
from .store import append_jsonl, read_json, write_json
from .tradelog import summarize, trade_log


def prepare(s, symbol: str, base, now: pd.Timestamp | None = None) -> pd.DataFrame:
    """Stored 5-minute bars -> entry-timeframe bars -> features (BTC as read-only context)."""
    b5 = load_bars(symbol, base, now)
    if len(b5) < 300:
        return pd.DataFrame()
    bars = resample_bars(b5, s.entry_minutes)
    ref = None
    if s.ref_symbol and s.ref_symbol != symbol:
        rb = load_bars(s.ref_symbol, base, now)
        if len(rb) >= 300:
            ref = resample_bars(rb, s.entry_minutes)
    return add_features(bars, ref, tf=s.entry_minutes)


def _all_symbols(s):
    return list(s.symbols) + ([s.ref_symbol] if s.ref_symbol and s.ref_symbol not in s.symbols else [])


def cmd_ingest(s, base, days: int, budget_min: float = 0) -> int:
    """Downloads history. With a time budget it stops cleanly when time is up; saved candles are kept and the next run resumes."""
    bad, unfinished = 0, []
    deadline = time.monotonic() + budget_min * 60 if budget_min and budget_min > 0 else None
    syms = _all_symbols(s)
    for i, sym in enumerate(syms):
        r = ingest(sym, days, base=base, deadline=deadline)
        print(f"{sym}: +{r['added']} bars, total {r['bars']}, last {r['last']}, missing {r['missing_pct']}% errors={r['errors']}"
              + ("  (time budget reached, will resume)" if r.get("partial") else ""))
        bad += 0 if r["ok"] else 1
        if r.get("partial"):
            unfinished.append(sym)
        if deadline is not None and time.monotonic() > deadline:
            unfinished += [x for x in syms[i + 1:]]
            break
    if unfinished:
        print("NOT FINISHED YET: " + ", ".join(unfinished) + ". Run 'Research and ingest' again to continue where it stopped (the daily run also continues it).")
    return 0 if bad == 0 else 1


def cmd_backtest(s, base, days: int) -> int:
    fam = s.family_tests()
    for sym in s.symbols:
        d = prepare(s, sym, base)
        if len(d) == 0 or len(d) < 90 * s.bars_per_day:
            print(f"{sym}: waiting for more history (need about 90 days; have {len(d) // max(s.bars_per_day, 1)}). Run 'Research and ingest' again.")
            continue
        out = base / sym
        out.mkdir(parents=True, exist_ok=True)
        rep = run_research(d, s, sym, engine=Engine(load_bars(sym, base), CRYPTO_TFS), family_size=fam)
        write_json(out / "backtest_report.json", rep)
        (out / "backtest_report.md").write_text(report_markdown(rep))
        t = trade_log(d, s, sym, days=days)
        t.to_csv(out / "trade_log_2y.csv", index=False)
        write_json(out / "trade_log_2y_summary.json", summarize(t, s, sym, days))
        print(f"{sym}: report written ({rep['data']['days']} days)")
        for n, r in rep["strategies"].items():
            o = r["out_of_sample_reported_once"]
            print(f"   {n:20s} OOS trades={o.get('trades', 0):4d} exp={o.get('net_expectancy_R')} verdict={r['verdict']}")
    return 0


def _alert_events(events, ledger_symbol, s, base):
    coin = ledger_symbol.split("-")[0]
    for e in events:
        k = e["type"]
        if k == "ENTRY_FILLED":
            send_alert(AlertType.ENTRY_TRIGGER, f"{coin}: practice entry filled at about ${e['entry']} ({e['label'].split('@')[0]}).", key=f"fill-{e['id']}", base=base)
        elif k == "ENTRY_CANCELLED":
            send_alert(AlertType.SYSTEM, f"{coin}: practice entry cancelled. {e['why']}", key=f"cancel-{e['id']}", base=base)
        elif k == "TARGET_REACHED":
            send_alert(AlertType.TARGET_REACHED, f"{coin}: target 1 reached (${e['t1']}). Sell half, move the stop to entry.", key=f"t1-{e['id']}", base=base)
        elif k.startswith("EXIT_"):
            kind = {"EXIT_STOP": AlertType.STOP_REACHED, "EXIT_TIME": AlertType.TIME_EXIT}.get(k, AlertType.TARGET_REACHED)
            send_alert(kind, f"{coin}: practice trade closed ({e['reason']}). Result {e['net_R']}R, about ${e['pnl_usd']}.", key=f"exit-{e['id']}", base=base)


def _gate(s, base, led: CryptoLedger, all_ledgers, now, rows_stale: bool, row: dict) -> str:
    paused, why = kill_switch(base)
    if paused:
        return f"paused ({why})"
    if rows_stale:
        return "data is stale"
    if row.get("plan_mode") == "chart_none":
        return "no clean chart-based plan (" + row.get("skip_reason", "") + ")"
    if row["blended_rr"] < s.min_blended_rr:
        return f"reward/risk {row['blended_rr']:.2f} is below the minimum {s.min_blended_rr}"
    if led.positions():
        return f"already holding a {led.symbol.split('-')[0]} practice trade"
    if sum(len(l.positions()) for l in all_ledgers) >= s.max_total_open:
        return "maximum open practice trades reached"
    if led.summary(now)["trades_today"] >= s.max_trades_per_day:
        return "daily trade limit reached"
    day_pnl = sum(l.summary(now)["realized_today_usd"] for l in all_ledgers)
    if day_pnl <= -s.account_equity * s.max_daily_loss_pct / 100:
        return "daily loss limit reached"
    return ""


def _still_loading(sym, base, now) -> bool:
    """True when stored history ends more than 3 days ago, i.e. the first big download for this coin is not finished."""
    raw = load_raw(sym, base)
    return len(raw) > 0 and (now - raw.index[-1]) > pd.Timedelta(days=3)


def cmd_evaluate(s, base, fetch: bool = True) -> int:
    now = now_utc()
    if fetch:   # top up the newest candles first (cheap: a day or two at most)
        for sym in _all_symbols(s):
            if _still_loading(sym, base, now):
                continue   # a big gap is the research job's work, never the 5-minute job's
            try:
                r = ingest(sym, 2, now=now, base=base, log=lambda *_: None)
                if not r["ok"]:
                    send_alert(AlertType.FEED_DISCONNECTED, f"{sym}: could not download new candles ({'; '.join(r['errors'][:1])}).",
                               key=f"feed-{sym}-{now.strftime('%Y%m%d%H')}", base=base)
            except Exception as e:  # noqa: BLE001
                print(f"{sym}: ingest failed: {type(e).__name__}")
    ledgers = [CryptoLedger(s, base, sym) for sym in s.symbols]
    status = {"generated_at": str(now), "symbols": {}}
    for led in ledgers:
        sym = led.symbol
        d = prepare(s, sym, base, now)
        info = {"ok": False}
        if _still_loading(sym, base, now):
            info["error"] = "history is still downloading - run 'Research and ingest' again"
            status["symbols"][sym] = info
            continue
        if len(d) < 100:
            info["error"] = "not enough stored data - run the research job first"
            status["symbols"][sym] = info
            continue
        last_close = d.index[-1] + pd.Timedelta(minutes=s.entry_minutes)
        age_min = (now - last_close).total_seconds() / 60
        stale = age_min > s.max_bar_age_min
        events = led.update(d, now)
        _alert_events(events, sym, s, base)
        lv = analyze(load_bars(sym, base, now), CRYPTO_TFS)
        warn = trend_break_warning(lv, long=True)
        if warn:
            for p_ in led.positions():
                if p_.get("filled_alerted"):
                    send_alert(AlertType.TREND_BREAK, f"{sym.split('-')[0]}: {warn}", key=f"brk-{p_['id']}", base=base)
        write_json(base / sym / "levels.json", lv)
        proven = proven_strategies(read_json(base / sym / "backtest_report.json", {})) if s.alert_only_proven else None
        info["proven"] = sorted(proven) if proven is not None else None
        rows = scan(s, d, sym, levels=lv, proven=proven)
        write_json(base / sym / "monitor.json", {"generated_at": str(now), "symbol": sym, "bar_close": str(last_close), "rows": rows})
        if stale:
            send_alert(AlertType.FEED_STALE, f"{sym}: newest completed candle is {age_min:.0f} minutes old.", key=f"stale-{sym}-{now.strftime('%Y%m%d%H')}", base=base)
        taken = []
        for r in rows:
            if r["status"] != "SIGNAL":
                continue
            key = f"sig-{sym}-{r['strategy']}-{r['bar_close']}"
            if r["kind"] == "Live practice":
                block = _gate(s, base, led, ledgers, now, stale, r)
                if block:
                    send_alert(AlertType.SIGNAL_NOT_TAKEN, "Signal, but no practice trade: " + block + ".\n" + signal_text(r, s), key=key, base=base)
                    continue
                inst_label = _label(r)
                plan = {"strategy": r["strategy"], "label": inst_label, "signal_time": str(d.index[-1]), "atr": r["atr"], "stop_atr": r["stop_atr"],
                        "t1_r": r["t1_r"], "t2_r": r["t2_r"], "max_hold_hours": r["max_hold_hours"], "units": r["units"], "regime": r["regime"],
                        "evidence_status": "EDGE_SUPPORTED_ON_PAST_DATA" if s.alert_only_proven else "NOT_PROVEN", "plan_mode": r.get("plan_mode", "atr")}
                if plan["plan_mode"] == "chart":
                    plan.update(stop_price=r["stop"], t1_price=r["target1"], t2_price=r["target2"])
                if led.open_position(plan):
                    taken.append(r["strategy"])
                    send_alert(AlertType.ENTRY_TRIGGER, "BUY signal - practice trade opened.\n" + signal_text(r, s), key=key, base=base)
            elif s.notify_research_signals:
                send_alert(AlertType.RESEARCH_SIGNAL, "RESEARCH ONLY (not proven, not a practice trade).\n" + signal_text(r, s), key=key, base=base)
            elif not s.alert_only_proven:
                send_alert(AlertType.RESEARCH_SIGNAL, "RESEARCH ONLY. " + signal_text(r, s), key=key, base=base, telegram=False)
            # else: a strategy that has not passed the fair test is shown on the dashboard only. No alert, no practice trade.
        info.update(ok=True, last_bar_close=str(last_close), age_min=round(age_min, 1), stale=stale, last_price=float(d.close.iloc[-1]),
                    regime=str(d.regime.iloc[-1]), taken=taken, **led.summary(now))
        status["symbols"][sym] = info
    paused, why = kill_switch(base)
    status["paused"], status["paused_reason"] = paused, why
    write_json(base / "status.json", status)
    append_jsonl(base / "run_log.jsonl", {"ts": str(now), "status": {k: v.get("ok") for k, v in status["symbols"].items()}})
    print(status)
    return 0


def _label(r):
    from .strategies import REGISTRY
    return REGISTRY[r["strategy"]]().label()


def cmd_telegram_test() -> int:
    if not telegram_enabled():
        ids, st = find_chat_ids()
        if st == "bad_token":
            print("CHAT ID NOT FOUND (bad_token). Telegram says the token is wrong. Check: " + token_shape())
            return 1
        if ids:
            print("FOUND YOUR CHAT ID: " + ", ".join(map(str, ids)) + "  -> put it in the TELEGRAM_CHAT_ID secret")
            return 0
        print(f"Telegram not configured yet ({st}). Add both secrets, then send your bot any message and run this again.")
        return 1
    r = send_telegram("Test message from your crypto paper-trading app. If you can read this, phone alerts work.")
    print("Telegram result:", r)
    if r in ("http_401", "http_404"):
        print("PROBLEM: Telegram does not accept the bot token. Re-copy it from BotFather (/mybots > your bot > API Token) "
              "into the TELEGRAM_BOT_TOKEN secret of THIS repo (Settings > Secrets and variables > Actions). "
              "What the saved token looks like (token itself hidden): " + token_shape())
    elif r == "http_400":
        print("PROBLEM: the token works but the chat number is wrong, or you have not sent your bot a message yet. "
              "Open your bot in Telegram, tap Start, send 'hi', then fix TELEGRAM_CHAT_ID (digits only).")
    elif r == "http_403":
        print("PROBLEM: the bot is blocked or was removed from that chat. Open the bot in Telegram, tap Start, and try again.")
    return 0 if r == "delivered" else 1


def cmd_status(s, base) -> int:
    print(read_json(base / "status.json", {}))
    for sym in _all_symbols(s):
        print(sym, gap_stats(sym, base))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="cryptoai")
    ap.add_argument("cmd", choices=["ingest", "backtest", "evaluate", "telegram-test", "status"])
    ap.add_argument("--days", type=int, default=730)
    ap.add_argument("--budget-min", type=float, default=0, help="stop downloading after this many minutes and resume next run (0 = no limit)")
    a = ap.parse_args(argv)
    s, base = load_settings(), state_dir()
    base.mkdir(parents=True, exist_ok=True)
    if a.cmd == "telegram-test":
        return cmd_telegram_test()
    return {"ingest": lambda: cmd_ingest(s, base, a.days, a.budget_min), "backtest": lambda: cmd_backtest(s, base, a.days),
            "evaluate": lambda: cmd_evaluate(s, base), "status": lambda: cmd_status(s, base)}[a.cmd]()


if __name__ == "__main__":
    sys.exit(main())
