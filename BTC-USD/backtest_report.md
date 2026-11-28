# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for BTC-USD. Long-only. Paper only.**

Data: BTC-USD 2024-10-18 00:00:00+00:00 to 2026-11-28 11:30:00+00:00 (772 days). Generated 2026-11-28 11:54:29.693639+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.02% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 199 | -0.813 | [-1.12, -0.444] | -0.029 | FAILED_OOS |
| donchian_breakout | 91 | -0.583 | [-1.03, -0.114] | -0.024 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 60 | -0.816 | [-1.373, -0.242] | -0.002 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 33 | -0.729 | [-1.231, -0.113] | -0.045 | INSUFFICIENT_SAMPLE |
| range_bounce | 76 | -1.001 | [-1.474, -0.512] | -0.014 | INSUFFICIENT_SAMPLE |
| btc_lead | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |
| support_bounce | 69 | -0.941 | [-1.484, -0.405] | -0.01 | INSUFFICIENT_SAMPLE |
| swing_breakout | 97 | -0.622 | [-1.012, -0.262] | -0.035 | INSUFFICIENT_SAMPLE |
| steady_scalper | 234 | -0.532 | [-0.669, -0.38] | -0.04 | FAILED_OOS |
| zone_rejection | 6 | -1.414 | [-2.212, 0.171] | -0.107 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 69 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 69, 'mean_difference_R': -0.019, 'ci_low': -0.204, 'ci_high': 0.167, 'atr_exp_R': -0.841, 'chart_exp_R': -0.859}

Baseline (1h trend, one trade a day) OOS: {'trades': 70, 'win_rate': 0.271, 'avg_win_R': 1.012, 'avg_loss_R': -1.675, 'gross_expectancy_R': -0.102, 'net_expectancy_R': -0.945, 'cost_per_trade_R': 0.843, 'total_net_R': -66.18, 'profit_factor': 0.23, 'max_drawdown_R': 64.76, 'longest_losing_streak': 8, 't_stat': -5.93, 'ci_level': 0.9996, 'ci_low': -1.47, 'ci_high': -0.379}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.