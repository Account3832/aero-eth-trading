# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for DOGE-USD. Long-only. Paper only.**

Data: DOGE-USD 2024-10-20 00:00:00+00:00 to 2026-11-28 11:30:00+00:00 (770 days). Generated 2026-11-28 11:55:26.320461+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 159 | -0.516 | [-0.848, -0.173] | -0.058 | FAILED_OOS |
| donchian_breakout | 65 | -0.367 | [-0.879, 0.217] | -0.042 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 35 | -0.568 | [-1.284, 0.256] | -0.032 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 28 | -0.319 | [-0.903, 0.336] | -0.003 | INSUFFICIENT_SAMPLE |
| range_bounce | 92 | -0.823 | [-1.146, -0.478] | -0.075 | INSUFFICIENT_SAMPLE |
| btc_lead | 6 | -0.59 | [-1.775, 0.767] | -0.019 | INSUFFICIENT_SAMPLE |
| support_bounce | 69 | -0.809 | [-1.226, -0.309] | -0.1 | INSUFFICIENT_SAMPLE |
| swing_breakout | 79 | -0.508 | [-0.923, -0.022] | -0.078 | INSUFFICIENT_SAMPLE |
| steady_scalper | 178 | -0.344 | [-0.521, -0.179] | -0.073 | FAILED_OOS |
| zone_rejection | 2 | 2.608 | [2.154, 3.063] | 1.161 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 47 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 47, 'mean_difference_R': 0.054, 'ci_low': -0.24, 'ci_high': 0.378, 'atr_exp_R': -0.487, 'chart_exp_R': -0.433}

Baseline (1h trend, one trade a day) OOS: {'trades': 55, 'win_rate': 0.491, 'avg_win_R': 0.979, 'avg_loss_R': -1.501, 'gross_expectancy_R': 0.315, 'net_expectancy_R': -0.284, 'cost_per_trade_R': 0.599, 'total_net_R': -15.61, 'profit_factor': 0.63, 'max_drawdown_R': 17.65, 'longest_losing_streak': 6, 't_stat': -1.56, 'ci_level': 0.9996, 'ci_low': -0.846, 'ci_high': 0.375}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.