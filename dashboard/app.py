"""Crypto Trading Terminal (ETH, AERO and the biggest coins): read-only dashboard. PAPER ONLY. Nothing here can place an order.

Reads state written by the scheduled jobs: a local folder (CRYPTOAI_STATE_DIR) or the repo's `data` branch
(CRYPTOAI_STATE_URL = https://raw.githubusercontent.com/<you>/<repo>/data).
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

for k in ("CRYPTOAI_STATE_URL",):  # Streamlit secrets -> env
    try:
        if k in st.secrets and not os.environ.get(k):
            os.environ[k] = str(st.secrets[k])
    except Exception:  # noqa: BLE001
        pass

from cryptoai import present as P
from cryptoai.config import load_settings
from cryptoai.data import resample_bars

S = load_settings()
st.set_page_config(page_title="Crypto Terminal", page_icon="📈", layout="wide")
GREEN, RED, AMBER = "#22c55e", "#ef4444", "#f59e0b"

st.markdown("""
<style>
.block-container{padding-top:2rem;max-width:1180px}
.app-title{font-size:1.9rem;font-weight:750;margin:0}
.app-sub{opacity:.65;margin:.2rem 0 .8rem 0}
.chip{display:inline-block;padding:3px 11px;border-radius:999px;font-size:.76rem;font-weight:650;margin:0 6px 6px 0;border:1px solid rgba(128,128,128,.35);background:rgba(128,128,128,.10)}
.chip.good{color:#22c55e}.chip.bad{color:#ef4444}.chip.warn{color:#f59e0b}
.kpi{border-radius:12px;padding:12px 16px;border:1px solid rgba(128,128,128,.28);background:rgba(128,128,128,.06)}
.kpi .label{font-size:.7rem;letter-spacing:.06em;text-transform:uppercase;opacity:.65;font-weight:650}
.kpi .value{font-size:1.5rem;font-weight:740}
.sig{border-radius:14px;padding:14px 18px;border:1px solid rgba(34,197,94,.55);background:rgba(34,197,94,.10);margin-bottom:10px}
</style>""", unsafe_allow_html=True)

st.markdown('<div class="app-title">Crypto Trading Terminal</div><div class="app-sub">Paper trading only. Nothing here places an order or touches an exchange.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Controls")
    sym = st.selectbox("Coin", list(S.symbols))
    st.caption("Runs 24/7. The scheduled job checks about every 5-10 minutes.")
    if st.button("Refresh now"):
        st.cache_data.clear()
    st.caption(f"Practice account: {P.money(S.account_equity, 0)}; risk per trade {S.max_risk_pct}% ({P.money(S.risk_usd, 0)}).")


@st.cache_data(ttl=60)
def status():
    return P.read_json_rel("status.json", {})


@st.cache_data(ttl=60)
def mon(sym):
    return P.read_json_rel(f"{sym}/monitor.json", {})


@st.cache_data(ttl=300)
def report(sym):
    return P.read_json_rel(f"{sym}/backtest_report.json", {})


@st.cache_data(ttl=300)
def log_summary(sym):
    return P.read_json_rel(f"{sym}/trade_log_2y_summary.json", {})


@st.cache_data(ttl=300)
def log_df(sym):
    return P.read_csv_rel(f"{sym}/trade_log_2y.csv")


@st.cache_data(ttl=120)
def paper(sym):
    return P.read_csv_rel(f"{sym}/paper_trades.csv")


@st.cache_data(ttl=120)
def open_pos(sym):
    return P.read_json_rel(f"{sym}/open_positions.json", [])


@st.cache_data(ttl=300)
def bars(sym):
    return P.read_bars_rel(sym)


stt = status()
info = (stt.get("symbols") or {}).get(sym, {})
c = st.columns(4)
def kpi(col, label, value):
    col.markdown(f'<div class="kpi"><div class="label">{label}</div><div class="value">{value}</div></div>', unsafe_allow_html=True)
kpi(c[0], f"{sym} last price", P.price(info.get("last_price"), sym) if info.get("ok") else "n/a")
kpi(c[1], "Market regime", str(info.get("regime", "n/a")))
kpi(c[2], "Data age", f"{info.get('age_min', 'n/a')} min" if info.get("ok") else "n/a")
kpi(c[3], "Open practice trades", info.get("open_count", 0))
if stt.get("paused"):
    st.error(f"Paused: {stt.get('paused_reason')}")
if info.get("stale"):
    st.warning("The newest candle is older than expected. Check the Data & health tab.")
if not info.get("ok"):
    st.info(info.get("error") or "No data yet. Run the 'Research and ingest' job in GitHub Actions first (see README).")

@st.cache_data(ttl=120)
def levels(sym):
    return P.read_json_rel(f"{sym}/levels.json", {})


def draw_levels(fig, lv, x0, x1, zones=True, lines=True, pivots=None):
    """Support/resistance bands, trendlines and swing points on a candlestick figure."""
    if zones:
        for z in lv.get("zones", []):
            col = {"support": GREEN, "resistance": RED}.get(z["role"], AMBER)
            fig.add_hrect(y0=z["low"], y1=z["high"], fillcolor=col, opacity=0.14 if z["strength"] != "Weak" else 0.07, line_width=0)
            fig.add_annotation(x=x1, y=z["mid"], text=f'{z["strength"]} {z["role"]}', showarrow=False, xanchor="right", font=dict(size=10, color=col), yshift=7)
    if lines:
        for l in lv.get("trendlines", []):
            fig.add_trace(go.Scatter(x=[pd.Timestamp(l["t1"]), pd.Timestamp(l["t_now"])], y=[l["p1"], l["p_now"]], mode="lines",
                                     line=dict(color=GREEN if l["kind"] == "support" else RED, dash="dash", width=1.2), name=f'{l["tf"]} {l["note"]}', showlegend=False))
    if pivots:
        pv = [q for q in lv.get("pivots", {}).get(pivots, []) if pd.Timestamp(q["time"]) >= x0]
        for kind, sym_, col in (("H", "triangle-down", RED), ("L", "triangle-up", GREEN)):
            pts = [q for q in pv if q["kind"] == kind]
            if pts:
                fig.add_trace(go.Scatter(x=[pd.Timestamp(q["time"]) for q in pts], y=[q["price"] for q in pts], mode="markers",
                                         marker=dict(symbol=sym_, size=9, color=col), showlegend=False, name="swing"))


tabs = st.tabs(["Monitor", "Levels & Trends", "Charts", "2-year results", "Reliability test", "Paper trades", "Data & health", "Logs"])

with tabs[0]:
    snap = []
    for c, i in (stt.get("symbols") or {}).items():
        snap.append({"Coin": c, "Price": P.price(i.get("last_price"), c) if i.get("last_price") else "n/a", "Trend": i.get("regime", ""),
                     "Strategies that passed the fair test": ", ".join(i.get("proven") or []) or "none yet", "Note": i.get("error", "")})
    if snap:
        st.markdown("**All coins at a glance.** A phone alert or practice trade happens only for a strategy listed as passed.")
        st.dataframe(pd.DataFrame(snap), hide_index=True, use_container_width=True)
    m = mon(sym)
    rows = m.get("rows", [])
    st.caption(f"Checked on candle closing {m.get('bar_close', 'n/a')} UTC. Every strategy is checked, including ones that have not been proven.")
    if not rows:
        st.write("Nothing to show yet.")
    for r in rows:
        if r["status"] == "SIGNAL":
            st.markdown(f'<div class="sig"><b>{"BUY signal" if r["kind"] == "Live practice" else "Idea only, not proven, no alert sent"}: {r["strategy"]}</b> ({r["kind"]})<br>'
                        f'Entry about {P.price(r["entry_ref"], sym)} (next candle) · Stop {P.price(r["stop"], sym)} · '
                        f'Target 1 {P.price(r["target1"], sym)} · Target 2 {P.price(r["target2"], sym)}<br>'
                        f'Size about {r["units"]} units ({P.money(r["notional_usd"], 0)}), risk about {P.money(r["risk_usd"], 0)}. Paper only.<br>'
                        f'{P.chart_plan_line(r, sym)}</div>', unsafe_allow_html=True)
    tbl = pd.DataFrame([{"Strategy": r["strategy"], "Type": r["kind"], "Status": r["status"], "Why": r["note"] or r["waiting_for"]} for r in rows])
    if len(tbl):
        st.dataframe(tbl, hide_index=True, use_container_width=True)

with tabs[1]:
    lv = levels(sym)
    if not lv.get("ok"):
        st.info("Not available yet. It appears after the 24/7 checker has run once with stored candles.")
    else:
        al = lv["alignment"]
        st.markdown(f"**Chart reading for {sym}** (as of {lv['asof']} UTC)")
        for line in lv["reading"]:
            st.write("- " + line)
        st.caption("Trends within trends: the biggest scale is first. A pullback inside a bigger uptrend is different from the same dip inside a downtrend. This describes the chart; it is not a promise.")
        ladder = pd.DataFrame([{"Scale": t_["label"], "Chart": t_["tf"], "Trend": t_["direction"], "Pattern": t_["pattern"], "Structure": t_["state"],
                                "Last swing high": t_["swing_high"], "Last swing low": t_["swing_low"], "Trend fails if price closes beyond": t_["invalidation"],
                                "Averages": t_["ema_state"]} for t_ in lv["timeframes"]])
        st.dataframe(ladder, hide_index=True, use_container_width=True)
        if any(t_.get("limited_history") for t_ in lv["timeframes"]):
            st.caption("Some scales have little history yet, so treat them as rough.")
        b5 = bars(sym)
        if len(b5):
            c1, c2 = st.columns(2)
            with c1:
                tfm = st.selectbox("Chart size", [15, 60, 240], index=1, format_func=lambda m: {15: "15 minutes", 60: "1 hour", 240: "4 hours"}[m], key="lv_tf")
            with c2:
                nb = st.slider("Candles to show", 60, 400, 160, key="lv_n")
            d = resample_bars(b5, tfm).iloc[-nb:]
            fig = go.Figure(go.Candlestick(x=d.index, open=d.open, high=d.high, low=d.low, close=d.close, increasing_line_color=GREEN, decreasing_line_color=RED))
            scale = {15: "Minor", 60: "Intermediate", 240: "Secondary"}[tfm]
            draw_levels(fig, lv, d.index[0], d.index[-1], pivots=scale)
            fig.update_layout(template="plotly_dark", height=560, xaxis_rangeslider_visible=False, margin=dict(l=10, r=10, t=20, b=10))
            ymin, ymax = float(d.low.min()), float(d.high.max())
            pad = (ymax - ymin) * 0.08
            fig.update_yaxes(range=[ymin - pad, ymax + pad])
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Green bands = support, red bands = resistance, amber = price is inside a zone. Triangles = confirmed swing points. Dashed lines = trendlines.")
        zt = pd.DataFrame([{"Type": z["role"], "From": z["low"], "To": z["high"], "Strength": z["strength"], "Touches": z["touches"], "Scales": ", ".join(z["tfs"]),
                            "Distance (ATR)": z["dist_atr"], "Note": z["former"] or ", ".join(z["labels"][:3])} for z in lv["zones"]])
        st.dataframe(zt, hide_index=True, use_container_width=True)


with tabs[2]:
    b5 = bars(sym)
    if len(b5) == 0:
        st.write("No stored candles yet.")
    else:
        hrs = st.slider("Hours to show", 6, 168, 48)
        tf = st.selectbox("Candle size (minutes)", [5, 15, 60], index=1)
        d = resample_bars(b5, tf).iloc[-int(hrs * 60 / tf):]
        fig = go.Figure(go.Candlestick(x=d.index, open=d.open, high=d.high, low=d.low, close=d.close, increasing_line_color=GREEN, decreasing_line_color=RED))
        if st.checkbox("Show support / resistance", value=True):
            draw_levels(fig, levels(sym), d.index[0], d.index[-1], lines=False)
        for p in open_pos(sym):
            fig.add_vline(x=pd.Timestamp(p["signal_time"]), line_color=AMBER, line_dash="dot")
        fig.update_layout(template="plotly_dark", height=520, xaxis_rangeslider_visible=False, margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    sm, t = log_summary(sym), log_df(sym)
    st.write("This replays each strategy's fixed rules over the last 2 years of saved candles, after fees and slippage. **It is a replay, not a prediction.** A win means the trade made money after costs.")
    if not sm.get("strategies"):
        st.info("Not available yet. Run the 'Research and ingest' job.")
    else:
        st.caption(f"Costs used: fee {sm['fee_pct_per_side']}% + slippage {sm['slippage_pct_per_side']}% per side; {sm['entry_candle_minutes']}-minute candles; illustrative risk {P.money(sm['risk_per_trade_usd_illustrative'], 0)} per trade.")
        st.dataframe(pd.DataFrame([{"Strategy": n, "Trades": v["trades"], "Win rate": v["win_rate"], "Avg cost (R)": v["avg_cost_R"], "Net per trade (R)": v["net_exp_R"],
                                    "Total (R)": v["total_net_R"], "Illustrative $": v["total_pnl_usd_illustrative"], "Worst losing streak": v.get("longest_losing_streak")}
                                   for n, v in sm["strategies"].items()]), hide_index=True, use_container_width=True)
        pick = st.selectbox("Show every trade for", list(sm["strategies"]))
        g = t[t.strategy == pick] if len(t) else t
        if len(g):
            cum = g.net_R.cumsum()
            fig = go.Figure(go.Scatter(x=pd.to_datetime(g.entry_time), y=cum, mode="lines", line=dict(color=GREEN if cum.iloc[-1] > 0 else RED)))
            fig.update_layout(template="plotly_dark", height=300, yaxis_title="Cumulative result (R)", margin=dict(l=10, r=10, t=20, b=10))
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(g[["date", "entry_time", "exit_time", "entry", "stop_price", "target1_price", "target2_price", "exit_price", "net_R", "result", "exit_reason"]].iloc[::-1],
                         hide_index=True, use_container_width=True)

with tabs[4]:
    rep = report(sym)
    if not rep:
        st.info("Not available yet. Run the 'Research and ingest' job.")
    else:
        st.write("The fair test: rules were fixed in advance (no tuning), then judged on the final quarter of the data that was never used to choose anything. Costs are included.")
        rows = []
        for n, r in rep["strategies"].items():
            o = r["out_of_sample_reported_once"]
            rows.append({"Strategy": n, "Fair-test trades": o.get("trades", 0), "Net per trade (R)": o.get("net_expectancy_R"),
                         "Range (CI)": f"[{o.get('ci_low')}, {o.get('ci_high')}]" if o.get("trades", 0) > 1 else "n/a",
                         "Break-even fee %/side": r["cost_sensitivity_out_of_sample"].get("breakeven_fee_pct"), "Verdict": P.verdict_plain(r["verdict"])})
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        st.caption(f"Buy-and-hold over the same fair-test period: {rep['data'].get('buy_and_hold_oos_pct')}%. Your fee assumption: {S.fee_pct}% per side. If a strategy's break-even fee is below what you really pay, it loses money.")
        ce = rep.get("chart_exits")
        if ce:
            st.subheader("Chart-based exits vs fixed exits")
            st.write(ce["question"])
            po = ce["pooled_out_of_sample"]
            if po.get("paired_trades"):
                st.write(f"Fair-test result on {po['paired_trades']} identical trades: fixed exits {po['atr_exp_R']} R per trade, chart exits {po['chart_exp_R']} R per trade "
                         f"(difference {po['mean_difference_R']} R, 95% range [{po['ci_low']}, {po['ci_high']}]). **{P.exit_verdict_plain(ce['verdict'])}**")
            else:
                st.write("Not enough trades with a clean chart plan yet.")
            rows_ = []
            for n_, v_ in ce["per_strategy"].items():
                a_ = v_["all_sample"]
                if a_.get("trades"):
                    rows_.append({"Strategy": n_, "Trades": a_["trades"], "Chart plan found": a_["with_chart_plan"], "Passed (no clean plan)": a_["skipped_no_clean_plan"],
                                  "Fixed exits (R/trade, same trades)": a_.get("atr_exp_R_same_trades"), "Chart exits (R/trade)": a_.get("chart_exp_R_same_trades"),
                                  "Main reason passed": max(a_["skip_reasons"], key=a_["skip_reasons"].get) if a_["skip_reasons"] else ""})
            if rows_:
                st.dataframe(pd.DataFrame(rows_), hide_index=True, use_container_width=True)
            st.caption("The chart method passes on trades with no room before resistance or no sensible stop, so it takes fewer trades. Per-strategy rows are descriptive only. To use chart exits for practice trades, set exit_mode: chart in config/settings.yaml.")
        for w in rep.get("warnings", []):
            st.warning(w)
        with st.expander("What this does not show"):
            for x in rep["limitations"]:
                st.write("- " + x)

with tabs[5]:
    pt, op = paper(sym), open_pos(sym)
    st.subheader("Open practice trades")
    st.dataframe(pd.DataFrame(op) if op else pd.DataFrame({"": ["None"]}), hide_index=True, use_container_width=True)
    st.subheader("Closed practice trades")
    if len(pt):
        st.metric("Total practice P&L", P.money(pt.pnl_usd.sum()))
        st.dataframe(pt.iloc[::-1], hide_index=True, use_container_width=True)
    else:
        st.write("None yet.")

with tabs[6]:
    st.json(stt or {"note": "no status yet"})
    b5 = bars(sym)
    if len(b5):
        st.write(f"Stored candles for {sym}: {len(b5):,}, from {b5.index[0]} to {b5.index[-1]}.")

with tabs[7]:
    st.write("Alert log (newest last). Phone messages go out only for practice-trade events and safety problems.")
    txt = P.read_text("alerts.jsonl")
    st.code("\n".join((txt or "no alerts yet").splitlines()[-30:]))
