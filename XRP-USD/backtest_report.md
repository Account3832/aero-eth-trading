# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for XRP-USD. Long-only. Paper only.**

Data: XRP-USD 2024-10-20 00:00:00+00:00 to 2026-11-14 10:15:00+00:00 (756 days). Generated 2026-11-14 10:34:27.711159+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 179 | -0.551 | [-0.872, -0.195] | -0.063 | FAILED_OOS |
| donchian_breakout | 84 | -0.263 | [-0.76, 0.3] | -0.003 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 37 | -0.475 | [-1.177, 0.485] | -0.003 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 23 | -0.486 | [-1.143, 0.337] | -0.04 | INSUFFICIENT_SAMPLE |
| range_bounce | 97 | -0.875 | [-1.216, -0.472] | -0.057 | INSUFFICIENT_SAMPLE |
| btc_lead | 5 | -0.834 | [-2.533, 0.485] | -0.011 | INSUFFICIENT_SAMPLE |
| support_bounce | 45 | -0.366 | [-1.004, 0.321] | 0.018 | INSUFFICIENT_SAMPLE |
| swing_breakout | 88 | -0.308 | [-0.764, 0.187] | -0.008 | INSUFFICIENT_SAMPLE |
| steady_scalper | 202 | -0.362 | [-0.532, -0.211] | -0.078 | FAILED_OOS |
| zone_rejection | 6 | -1.275 | [-1.401, -1.135] | -0.48 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 58 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 58, 'mean_difference_R': -0.044, 'ci_low': -0.274, 'ci_high': 0.178, 'atr_exp_R': -0.517, 'chart_exp_R': -0.562}

Baseline (1h trend, one trade a day) OOS: {'trades': 54, 'win_rate': 0.519, 'avg_win_R': 1.134, 'avg_loss_R': -1.385, 'gross_expectancy_R': 0.489, 'net_expectancy_R': -0.079, 'cost_per_trade_R': 0.568, 'total_net_R': -4.25, 'profit_factor': 0.88, 'max_drawdown_R': 10.71, 'longest_losing_streak': 5, 't_stat': -0.41, 'ci_level': 0.9996, 'ci_low': -0.739, 'ci_high': 0.57}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.