# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for AVAX-USD. Long-only. Paper only.**

Data: AVAX-USD 2024-10-20 00:00:00+00:00 to 2026-11-14 10:15:00+00:00 (756 days). Generated 2026-11-14 10:35:58.768889+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 14 | -0.659 | [-1.352, 0.277] | -0.146 | INSUFFICIENT_SAMPLE |
| donchian_breakout | 8 | -0.408 | [-1.307, 1.728] | -0.121 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 2 | 0.294 | [-1.426, 2.015] | 0.202 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 8 | -0.635 | [-1.319, 0.437] | -0.193 | INSUFFICIENT_SAMPLE |
| range_bounce | 12 | -0.638 | [-1.49, 0.27] | -0.072 | INSUFFICIENT_SAMPLE |
| btc_lead | 1 | -0.701 | n/a | -0.203 | INSUFFICIENT_SAMPLE |
| support_bounce | 4 | -1.378 | [-1.639, -1.223] | -0.355 | INSUFFICIENT_SAMPLE |
| swing_breakout | 9 | -0.627 | [-1.285, 0.763] | -0.201 | INSUFFICIENT_SAMPLE |
| steady_scalper | 16 | -0.311 | [-0.852, 0.206] | -0.092 | INSUFFICIENT_SAMPLE |
| zone_rejection | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 8 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 8, 'mean_difference_R': -0.59, 'ci_low': -1.012, 'ci_high': -0.169, 'atr_exp_R': 0.161, 'chart_exp_R': -0.428}

Baseline (1h trend, one trade a day) OOS: {'trades': 5, 'win_rate': 0.4, 'avg_win_R': 1.238, 'avg_loss_R': -1.385, 'gross_expectancy_R': 0.071, 'net_expectancy_R': -0.336, 'cost_per_trade_R': 0.407, 'total_net_R': -1.68, 'profit_factor': 0.6, 'max_drawdown_R': 1.37, 'longest_losing_streak': 2, 't_stat': -0.49, 'ci_level': 0.9996, 'ci_low': -1.483, 'ci_high': 1.561}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.