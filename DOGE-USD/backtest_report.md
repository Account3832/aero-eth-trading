# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for DOGE-USD. Long-only. Paper only.**

Data: DOGE-USD 2024-10-20 00:00:00+00:00 to 2026-11-14 10:15:00+00:00 (756 days). Generated 2026-11-14 10:35:09.992686+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 159 | -0.531 | [-0.862, -0.223] | -0.064 | FAILED_OOS |
| donchian_breakout | 67 | -0.42 | [-0.958, 0.171] | -0.064 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 35 | -0.572 | [-1.324, 0.225] | -0.032 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 29 | -0.246 | [-0.794, 0.385] | 0.02 | INSUFFICIENT_SAMPLE |
| range_bounce | 86 | -0.833 | [-1.217, -0.403] | -0.072 | INSUFFICIENT_SAMPLE |
| btc_lead | 7 | -0.685 | [-1.698, 0.582] | -0.051 | INSUFFICIENT_SAMPLE |
| support_bounce | 64 | -0.826 | [-1.258, -0.32] | -0.102 | INSUFFICIENT_SAMPLE |
| swing_breakout | 76 | -0.495 | [-0.914, 0.028] | -0.072 | INSUFFICIENT_SAMPLE |
| steady_scalper | 174 | -0.353 | [-0.513, -0.198] | -0.079 | FAILED_OOS |
| zone_rejection | 3 | 1.233 | [-1.518, 3.063] | 0.508 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 47 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 47, 'mean_difference_R': 0.093, 'ci_low': -0.188, 'ci_high': 0.395, 'atr_exp_R': -0.547, 'chart_exp_R': -0.453}

Baseline (1h trend, one trade a day) OOS: {'trades': 54, 'win_rate': 0.5, 'avg_win_R': 0.98, 'avg_loss_R': -1.489, 'gross_expectancy_R': 0.336, 'net_expectancy_R': -0.255, 'cost_per_trade_R': 0.591, 'total_net_R': -13.75, 'profit_factor': 0.66, 'max_drawdown_R': 13.32, 'longest_losing_streak': 4, 't_stat': -1.39, 'ci_level': 0.9996, 'ci_low': -0.816, 'ci_high': 0.287}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.