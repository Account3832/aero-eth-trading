"""Backtesting engine for crypto SPOT, long-only. Researches PRICE signals only.

Rules that prevent flattering results:
  * signal at the bar close, entry at the NEXT bar's open, plus slippage
  * ambiguous bars (stop and target both reachable) resolve to the STOP
  * targets need a trade-through of the slippage buffer to count
  * T2 can only fill on a bar after T1, and the stop moves to breakeven only for later bars
  * exchange fees are charged on both sides of every trade
  * parameters are fixed a priori (no parameter search); the final out-of-sample block is reported once
  * every result is also shown at other fee levels, because fees decide whether short-term crypto trading can work
"""
from __future__ import annotations

from collections import defaultdict

import numpy as np
import pandas as pd

from .config import Settings
from .levels import confluence_check, structure_plan
from .strategies import BASELINE, REGISTRY, Strategy

FEE_LEVELS = (0.0, 0.02, 0.05, 0.10, 0.20, 0.40)   # % per side, for the sensitivity table


def resolve_trade(o, h, l, c, i0, e_ref, entry, risk, stop, t1, t2, slip, max_hold, data_end_closes=True) -> dict:
    """Walk bars from the entry bar i0 and resolve one long position in two halves (T1 half, T2 half).

    Shared by the backtester and the paper ledger so both use identical, conservative rules. Returns price
    differences averaged over the two halves. `closed` is False only when the bars ran out first and
    data_end_closes is False (the position is still open)."""
    n = len(o)
    buf = slip
    stop_cur, t1_bar = stop, None
    open_halves = {1: True, 2: True}
    acc = {"gross": 0.0, "net": 0.0}
    reasons, last_j = {}, i0

    def close_half(which, ref_px, fill_px, why):
        open_halves[which] = False
        acc["gross"] += 0.5 * (ref_px - e_ref)
        acc["net"] += 0.5 * (fill_px - entry)
        reasons[which] = why

    j = i0
    while j < n and any(open_halves.values()):
        last_j = j
        if j - i0 >= max_hold:
            for w in (1, 2):
                if open_halves[w]:
                    close_half(w, o[j], o[j] - slip, "maxhold")
            break
        if l[j] <= stop_cur:  # conservative: the stop wins any ambiguous bar
            lvl = min(stop_cur, o[j])  # a gap through the stop fills at the open
            be = stop_cur == entry
            for w in (1, 2):
                if open_halves[w]:
                    close_half(w, lvl, lvl - slip, "BE-stop" if be else "stop")
            break
        if open_halves[1] and h[j] >= t1 + buf:
            close_half(1, t1, t1, "T1")
            stop_cur, t1_bar = entry, j  # breakeven applies from the NEXT bar
        elif (not open_halves[1]) and open_halves[2] and t1_bar is not None and j > t1_bar and h[j] >= t2 + buf:
            close_half(2, t2, t2, "T2")
        j += 1
    still_open = any(open_halves.values())
    if still_open and data_end_closes:
        for w in (1, 2):
            if open_halves[w]:
                close_half(w, c[last_j], c[last_j] - slip, "data_end")
        still_open = False
    return {"closed": not still_open, "gross": acc["gross"], "net": acc["net"], "reasons": reasons,
            "last_j": last_j, "halves_open": dict(open_halves)}


COLS = ["strategy", "label", "date", "signal_time", "entry_time", "exit_time", "dir", "entry", "risk", "gross_R", "net_R",
        "exit_reason", "regime", "utc_block", "trigger"]


def _plan_for(engine, d, i, s, entry, atr_i, strat, a=None):
    """Chart-based stop and targets at signal bar i, using only candles complete at that bar's close."""
    a = a if a is not None else engine.at(d.index[i] + pd.Timedelta(minutes=s.entry_minutes), full=False)
    params = s.struct_params()
    if getattr(strat, "min_room_r", None):
        params["min_room_r"] = strat.min_room_r
    return structure_plan(a, entry, atr_i, True, **params)


def simulate(d: pd.DataFrame, strat: Strategy, s: Settings, symbol: str, dates: set | None = None, engine=None, exit_mode: str = "atr",
             skips: list | None = None) -> pd.DataFrame:
    """exit_mode "chart" needs `engine` (levels.Engine) and takes stop/targets from support and resistance zones; trades with no clean
    chart plan are passed (their reasons are appended to `skips`)."""
    chart_strat = bool(getattr(strat, "needs_chart", False))
    if chart_strat and engine is None:
        return pd.DataFrame([], columns=COLS)      # a chart-checklist strategy cannot be tested without the chart engine
    sig = strat.signals(d)
    dirs = sig["dir"].values
    n = len(d)
    o, h, l, c = d.open.values, d.high.values, d.low.values, d.close.values
    atr = d.atr.values
    date = d.date.values
    idx = d.index
    slip_f, fee_f = s.slip_pct(symbol) / 100.0, s.fee_pct / 100.0
    max_hold = max(int(strat.max_hold_hours * 60 / s.entry_minutes), 1)
    trades, busy_until, per_day = [], -1, defaultdict(int)
    for i in np.flatnonzero(dirs != 0):
        if i <= busy_until or i + 1 >= n:
            continue
        dte = date[i]
        if dates is not None and dte not in dates:
            continue
        if per_day[dte] >= s.max_trades_per_day or not np.isfinite(atr[i]) or atr[i] <= 0:
            continue
        e_ref = o[i + 1]
        slip = slip_f * e_ref
        entry = e_ref + slip
        risk = strat.stop_atr * atr[i]
        stop, t1, t2 = entry - risk, entry + strat.t1_r * risk, entry + strat.t2_r * risk
        if exit_mode == "chart" or chart_strat:
            a_i = engine.at(idx[i] + pd.Timedelta(minutes=s.entry_minutes), full=False)
            if chart_strat:
                cf = confluence_check(a_i, entry, atr[i], l[i], c[i])
                if not cf["ok"]:
                    if skips is not None:
                        skips.append({"strategy": strat.name, "signal_time": idx[i], "date": dte, "reason": cf["why"]})
                    continue
            pl = _plan_for(engine, d, i, s, entry, atr[i], strat, a_i)
            if not pl["ok"]:
                if skips is not None:
                    skips.append({"strategy": strat.name, "signal_time": idx[i], "date": dte, "reason": pl["fail"]})
                continue
            risk, stop, t1, t2 = pl["risk"], pl["stop"], pl["t1"], pl["t2"]
        res = resolve_trade(o, h, l, c, i + 1, e_ref, entry, risk, stop, t1, t2, slip, max_hold)
        fee_px = 2 * fee_f * entry     # entry plus exit, per unit
        gross, net, last_j = res["gross"], res["net"] - fee_px, res["last_j"]
        r = res["reasons"]
        trades.append({
            "strategy": strat.name, "label": strat.label(), "date": dte, "signal_time": idx[i], "entry_time": idx[i + 1],
            "exit_time": idx[last_j], "dir": 1, "entry": entry, "risk": risk, "gross_R": gross / risk, "net_R": net / risk,
            "exit_reason": f"{r.get(1, '')}|{r.get(2, '')}", "regime": d.regime.values[i], "utc_block": d.utc_block.values[i],
            "trigger": sig["trigger"].values[i]})
        busy_until = last_j + s.cooldown_bars
        per_day[dte] += 1
    return pd.DataFrame(trades, columns=COLS)


def _paired_outcome(d, i, strat, s, symbol, engine):
    """Outcome of the SAME entry under chart-based exits. Returns (net_R, reason_if_skipped)."""
    o, h, l, c, atr = d.open.values, d.high.values, d.low.values, d.close.values, d.atr.values
    slip_f, fee_f = s.slip_pct(symbol) / 100.0, s.fee_pct / 100.0
    e_ref = o[i + 1]
    slip = slip_f * e_ref
    entry = e_ref + slip
    pl = _plan_for(engine, d, i, s, entry, atr[i], strat)
    if not pl["ok"]:
        return None, pl["fail"]
    max_hold = max(int(strat.max_hold_hours * 60 / s.entry_minutes), 1)
    res = resolve_trade(o, h, l, c, i + 1, e_ref, entry, pl["risk"], pl["stop"], pl["t1"], pl["t2"], slip, max_hold)
    return (res["net"] - 2 * fee_f * entry) / pl["risk"], ""


def _reason_bucket(r: str) -> str:
    return ("no room before resistance" if "away (needs" in r else "stop would be too wide" if "too far" in r else
            "no support zone for a stop" if "no support" in r else "chart analysis unavailable")


def compare_exits(d: pd.DataFrame, s: Settings, symbol: str, names: list[str], engine, sp: dict | None = None) -> dict:
    """Paired test: the SAME entries scored with fixed ATR exits versus chart-based exits. One pre-declared hypothesis
    (chart exits earn more per trade at equal dollar risk), tested on the pooled live strategies, so no multiple-testing penalty is needed.
    Per-strategy rows are descriptive only."""
    sp = sp or chrono_split(sorted(set(d.date)))
    oos_dates = set(sp["oos"])
    per, pool = {}, {"all": [], "oos": []}
    for n in names:
        strat = REGISTRY[n]()
        t = simulate(d, strat, s, symbol)
        rows = []
        for r in t.itertuples():
            i = d.index.get_loc(r.signal_time)
            net_c, why = _paired_outcome(d, i, strat, s, symbol, engine)
            rows.append({"date": r.date, "atr": float(r.net_R), "chart": net_c, "why": why})
        df = pd.DataFrame(rows, columns=["date", "atr", "chart", "why"])

        def stats(x: pd.DataFrame) -> dict:
            if len(x) == 0:
                return {"trades": 0}
            ok = x[x.chart.notna()]
            skipped = x[x.chart.isna()]
            out = {"trades": int(len(x)), "with_chart_plan": int(len(ok)), "skipped_no_clean_plan": int(len(skipped)),
                   "skip_reasons": skipped.why.map(_reason_bucket).value_counts().to_dict(),
                   "atr_exp_R_all": round(float(x.atr.mean()), 3), "atr_total_R_all": round(float(x.atr.sum()), 1)}
            if len(ok):
                diff = (ok.chart - ok.atr).values.astype(float)
                lo, hi = boot_ci(diff, 0.95)
                out.update(atr_exp_R_same_trades=round(float(ok.atr.mean()), 3), chart_exp_R_same_trades=round(float(ok.chart.mean()), 3),
                           mean_difference_R=round(float(diff.mean()), 3), diff_ci_low=round(lo, 3), diff_ci_high=round(hi, 3),
                           chart_total_R_skips_as_zero=round(float(ok.chart.sum()), 1), chart_win_rate=round(float((ok.chart > 0).mean()), 3),
                           atr_win_rate_same_trades=round(float((ok.atr > 0).mean()), 3))
            return out
        oos = df[df.date.isin(oos_dates)]
        per[n] = {"all_sample": stats(df), "out_of_sample": stats(oos)}
        pool["all"].append(df[df.chart.notna()])
        pool["oos"].append(oos[oos.chart.notna()])

    def pooled(frames) -> dict:
        x = pd.concat(frames) if frames else pd.DataFrame(columns=["atr", "chart"])
        if len(x) == 0:
            return {"paired_trades": 0}
        diff = (x.chart - x.atr).values.astype(float)
        lo, hi = boot_ci(diff, 0.95)
        return {"paired_trades": int(len(x)), "mean_difference_R": round(float(diff.mean()), 3), "ci_low": round(lo, 3), "ci_high": round(hi, 3),
                "atr_exp_R": round(float(x.atr.mean()), 3), "chart_exp_R": round(float(x.chart.mean()), 3)}
    p_oos, p_all = pooled(pool["oos"]), pooled(pool["all"])
    n = p_oos.get("paired_trades", 0)
    if n < s.min_trades_for_claim:
        verdict, why = "INSUFFICIENT_SAMPLE", f"only {n} paired out-of-sample trades; at least {s.min_trades_for_claim} are needed"
    elif p_oos["ci_low"] > 0:
        verdict, why = "CHART_EXITS_BETTER", "the 95% range for the per-trade difference is above zero (still only past data)"
    elif p_oos["ci_high"] < 0:
        verdict, why = "CHART_EXITS_WORSE", "the 95% range for the per-trade difference is below zero"
    else:
        verdict, why = "NOT_DEMONSTRATED", "the 95% range for the per-trade difference includes zero"
    return {"question": "At the same dollar risk per trade, do stops and targets taken from support/resistance zones earn more than fixed ATR exits on the same entries?",
            "pooled_out_of_sample": p_oos, "pooled_all_sample": p_all, "verdict": verdict, "verdict_reason": why, "per_strategy": per,
            "notes": ["Compared on identical entries; R is measured against each method's own stop, so both risk the same dollars per trade.",
                      "Trades with no clean chart plan are passed by the chart method; see the skip counts and the 'skips as zero' totals.",
                      "Chart zones at each entry use only candles that had closed by then."]}


# ---------------------------------------------------------------- metrics

def boot_ci(r: np.ndarray, level: float = 0.95, n_boot: int = 2000, seed: int = 7):
    """Percentile bootstrap CI of the mean. Ignores serial correlation between trades; treat as optimistic."""
    if len(r) < 2:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    means = rng.choice(r, size=(n_boot, len(r)), replace=True).mean(axis=1)
    a = (1 - level) / 2
    return (float(np.quantile(means, a)), float(np.quantile(means, 1 - a)))


def metrics(t: pd.DataFrame, level: float = 0.95) -> dict:
    if t is None or len(t) == 0:
        return {"trades": 0}
    r = t.net_R.values.astype(float)
    g = t.gross_R.values.astype(float)
    wins, losses = r[r > 0], r[r <= 0]
    cum = np.cumsum(r)
    dd = float((np.maximum.accumulate(cum) - cum).max())
    streak = cur = 0
    for x in r:
        cur = cur + 1 if x <= 0 else 0
        streak = max(streak, cur)
    lo, hi = boot_ci(r, level)
    sd = r.std(ddof=1) if len(r) > 1 else float("nan")
    return {"trades": int(len(r)), "win_rate": round(float((r > 0).mean()), 3),
            "avg_win_R": round(float(wins.mean()), 3) if len(wins) else 0.0,
            "avg_loss_R": round(float(losses.mean()), 3) if len(losses) else 0.0,
            "gross_expectancy_R": round(float(g.mean()), 3), "net_expectancy_R": round(float(r.mean()), 3),
            "cost_per_trade_R": round(float((g - r).mean()), 3), "total_net_R": round(float(r.sum()), 2),
            "profit_factor": round(float(wins.sum() / abs(losses.sum())), 2) if losses.sum() < 0 else None,
            "max_drawdown_R": round(dd, 2), "longest_losing_streak": int(streak),
            "t_stat": round(float(r.mean() / (sd / np.sqrt(len(r)))), 2) if sd and sd > 0 else None,
            "ci_level": round(level, 4), "ci_low": round(lo, 3), "ci_high": round(hi, 3)}


def by(t: pd.DataFrame, col: str) -> dict:
    return {str(k): {m: v for m, v in metrics(g).items() if m in ("trades", "net_expectancy_R", "win_rate", "total_net_R")}
            for k, g in t.groupby(col)} if len(t) else {}


def cost_table(t: pd.DataFrame, base_fee_pct: float, fees=FEE_LEVELS) -> dict:
    """The same trades re-scored at other fee levels (fees are charged on entry value, so this is exact).
    Also solves for the fee at which the average trade breaks even."""
    if t is None or len(t) == 0:
        return {"rows": [], "breakeven_fee_pct": None}
    ratio = (t.entry / t.risk).values.astype(float)
    net = t.net_R.values.astype(float)
    rows = []
    for f in fees:
        r = net + 2 * (base_fee_pct - f) / 100.0 * ratio
        rows.append({"fee_pct": f, "net_expectancy_R": round(float(r.mean()), 3), "win_rate": round(float((r > 0).mean()), 3),
                     "total_net_R": round(float(r.sum()), 1)})
    slope = 0.02 * float(ratio.mean())
    be = base_fee_pct + float(net.mean()) / slope if slope > 0 else None
    return {"rows": rows, "breakeven_fee_pct": None if be is None else round(be, 3),
            "note": "Fee per side as % of trade value. If the break-even fee is below your real fee, the average trade loses money."}


# ----------------------------------------------------------------- splits

def chrono_split(dates: list, frac=(0.5, 0.25, 0.25)) -> dict:
    n = len(dates)
    a, b = int(n * frac[0]), int(n * (frac[0] + frac[1]))
    return {"train": dates[:a], "val": dates[a:b], "oos": dates[b:]}


def walk_forward_folds(dates: list, test_days: int = 30, min_train: int = 60) -> list[dict]:
    out = []
    for s0 in range(min_train, len(dates), test_days):
        test = dates[s0:s0 + test_days]
        if len(test) >= max(5, test_days // 2):
            out.append({"train_end": str(dates[s0 - 1]), "test_start": str(test[0]), "test_end": str(test[-1]), "test_dates": test})
    return out


def _slice(t: pd.DataFrame, dates) -> pd.DataFrame:
    ds = set(dates)
    return t[t["date"].isin(ds)] if len(t) else t


def edge_verdict(oos: dict, folds_pos_frac: float | None, base_oos_exp: float | None, min_trades: int) -> tuple[str, str]:
    n = oos.get("trades", 0)
    if n < min_trades:
        return "INSUFFICIENT_SAMPLE", f"only {n} out-of-sample trades; at least {min_trades} are required before any claim"
    exp, lo, hi = oos["net_expectancy_R"], oos["ci_low"], oos["ci_high"]
    if exp <= 0 and hi < 0:
        return "FAILED_OOS", f"out-of-sample net expectancy {exp}R and the CI upper bound {hi}R is below zero"
    if exp > 0 and lo > 0 and (folds_pos_frac or 0) >= 0.6 and (base_oos_exp is None or exp > base_oos_exp):
        return "EDGE_SUPPORTED", "positive net expectancy with a CI above zero, positive in most folds, and it beats the baseline. Still only price evidence on past data"
    return "NOT_DEMONSTRATED", f"out-of-sample net expectancy {exp}R, CI [{lo}, {hi}]; no reliable edge shown"


# --------------------------------------------------------------- research

def run_research(d: pd.DataFrame, s: Settings, symbol: str, strategy_names=None, engine=None, family_size: int | None = None) -> dict:
    names = list(strategy_names or (*s.enabled_strategies, *s.research_only_strategies))
    if engine is None:
        names = [n for n in names if not getattr(REGISTRY[n], "needs_chart", False)]
    dates = sorted(set(d.date))
    sp = chrono_split(dates)
    fam = max(int(family_size or 0), len(names), 1)   # every strategy-by-coin test in the study, not just this coin
    level = 1 - 0.05 / fam                             # Bonferroni across the whole family
    warnings = []
    if len(dates) < 120:
        warnings.append(f"Only {len(dates)} days of data. Results are very noisy at this size. Run 'Daily ingest and backtest' to build history.")
    base_t = simulate(d, BASELINE(), s, symbol)
    base_oos = metrics(_slice(base_t, sp["oos"]), level)
    folds = walk_forward_folds(dates)
    results = {}
    for name in names:
        strat = REGISTRY[name]()
        t = simulate(d, strat, s, symbol, engine=engine)
        oos_t = _slice(t, sp["oos"])
        oos = metrics(oos_t, level)
        fold_res = []
        for f in folds:
            m = metrics(_slice(t, f["test_dates"]), level)
            fold_res.append({"test": f"{f['test_start']}..{f['test_end']}", "trades": m["trades"], "net_expectancy_R": m.get("net_expectancy_R")})
        scored = [f for f in fold_res if f["trades"] > 0]
        pos_frac = (sum(1 for f in scored if f["net_expectancy_R"] > 0) / len(scored)) if scored else None
        entry = {"label": strat.label(), "spec": {k: v for k, v in strat.spec.__dict__.items() if k != "params"},
                 "stop_atr": strat.stop_atr, "t1_r": strat.t1_r, "t2_r": strat.t2_r, "blended_rr": strat.blended_rr,
                 "all_sample_in_sample_reference": metrics(t, level),
                 "train": metrics(_slice(t, sp["train"]), level), "validation": metrics(_slice(t, sp["val"]), level),
                 "out_of_sample_reported_once": oos, "walk_forward_folds": fold_res, "folds_positive_fraction": pos_frac,
                 "by_regime_descriptive": by(t, "regime"), "by_time_block_descriptive": by(t, "utc_block"),
                 "cost_sensitivity_out_of_sample": cost_table(oos_t, s.fee_pct), "cost_sensitivity_all_sample": cost_table(t, s.fee_pct)}
        if len(t):
            by_day = t.groupby("date").net_R.sum()
            tot = by_day.sum()
            entry["top_day_share_of_total_R"] = round(float(by_day.max() / tot), 2) if tot > 0 else None
        verdict, why = edge_verdict(oos, pos_frac, base_oos.get("net_expectancy_R"), s.min_trades_for_claim)
        entry["verdict"], entry["verdict_reason"] = verdict, why
        results[name] = entry
    oos_dates = sp["oos"]
    bh = None
    if oos_dates:
        seg = d[d.date.isin(set(oos_dates))]
        if len(seg) > 1:
            bh = round(float(seg.close.iloc[-1] / seg.open.iloc[0] - 1) * 100, 1)
    return {
        "report_type": f"CRYPTO SPOT PRICE-SIGNAL RESEARCH for {symbol}. Long-only. Paper only.",
        "symbol": symbol, "generated_at": str(pd.Timestamp.now(tz="UTC")),
        "data": {"first": str(d.index[0]), "last": str(d.index[-1]), "bars": int(len(d)), "days": len(dates),
                 "splits_days": {k: len(v) for k, v in sp.items()}, "buy_and_hold_oos_pct": bh},
        "assumptions": {"entry_candle_minutes": s.entry_minutes, "fee_pct_per_side": s.fee_pct, "slippage_pct_per_side": s.slip_pct(symbol), "entry": "next bar open + slippage",
                        "ambiguous_bars": "stop first", "target_fill": "requires trade-through by the slippage buffer",
                        "max_trades_per_day": s.max_trades_per_day, "cooldown_minutes": s.cooldown_min, "direction": "long only (spot)"},
        "baseline_1h_trend": {"out_of_sample": base_oos, "all_sample": metrics(base_t, level)},
        "chart_exits": compare_exits(d, s, symbol, [n for n in names if n in s.enabled_strategies], engine, sp) if engine is not None else None,
        "strategies": results,
        "multiple_testing": {"strategies_evaluated": len(names), "family_size": fam, "ci_level_used": round(level, 5),
                             "note": f"Bonferroni-adjusted across all {fam} strategy-by-coin tests, so adding coins makes the pass bar stricter. No parameter search was run, so nothing was tuned on the data."},
        "warnings": warnings,
        "limitations": ["Bootstrap CIs ignore serial correlation between trades.",
                        "AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.",
                        "Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.",
                        "Only one market regime may be covered; crypto cycles are long.",
                        "Past results do not predict future results."]}


def report_markdown(rep: dict) -> str:
    L = ["# Crypto backtest report", f"**{rep['report_type']}**", "",
         f"Data: {rep['symbol']} {rep['data']['first']} to {rep['data']['last']} ({rep['data']['days']} days). Generated {rep['generated_at']}.",
         f"Entry candles: {rep['assumptions']['entry_candle_minutes']} minutes. Costs assumed: fee {rep['assumptions']['fee_pct_per_side']}% + slippage {rep['assumptions']['slippage_pct_per_side']}% per side.", ""]
    for w in rep["warnings"]:
        L.append(f"> WARNING: {w}")
    L += ["", "| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |", "|---|---|---|---|---|---|"]
    for n, r in rep["strategies"].items():
        o = r["out_of_sample_reported_once"]
        ci = f"[{o.get('ci_low')}, {o.get('ci_high')}]" if o.get("trades", 0) > 1 else "n/a"
        be = r["cost_sensitivity_out_of_sample"].get("breakeven_fee_pct")
        L.append(f"| {n} | {o.get('trades', 0)} | {o.get('net_expectancy_R', 'n/a')} | {ci} | {be if be is not None else 'n/a'} | {r['verdict']} |")
    ce = rep.get("chart_exits")
    if ce:
        po = ce["pooled_out_of_sample"]
        L += ["", "## Chart-based exits vs fixed exits (same entries)", f"Verdict: **{ce['verdict']}** - {ce['verdict_reason']}",
              f"Pooled out-of-sample: {po}"]
    L += ["", f"Baseline (1h trend, one trade a day) OOS: {rep['baseline_1h_trend']['out_of_sample']}", "", "Limitations:"]
    L += [f"- {x}" for x in rep["limitations"]]
    return "\n".join(L)
