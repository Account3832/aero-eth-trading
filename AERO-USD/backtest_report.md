# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for AERO-USD. Long-only. Paper only.**

Data: AERO-USD 2024-10-18 00:00:00+00:00 to 2026-11-14 10:15:00+00:00 (758 days). Generated 2026-11-14 10:33:40.385235+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.1% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 202 | -0.229 | [-0.546, 0.092] | -0.019 | NOT_DEMONSTRATED |
| donchian_breakout | 84 | -0.342 | [-0.765, 0.146] | -0.152 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 39 | -0.558 | [-1.079, 0.117] | -0.118 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 22 | -0.473 | [-1.055, 0.196] | -0.118 | INSUFFICIENT_SAMPLE |
| range_bounce | 91 | -0.641 | [-1.051, -0.222] | -0.104 | INSUFFICIENT_SAMPLE |
| btc_lead | 7 | -0.514 | [-1.4, 1.088] | -0.193 | INSUFFICIENT_SAMPLE |
| support_bounce | 50 | -0.108 | [-0.71, 0.6] | 0.049 | INSUFFICIENT_SAMPLE |
| swing_breakout | 94 | -0.112 | [-0.569, 0.33] | 0.024 | INSUFFICIENT_SAMPLE |
| steady_scalper | 221 | -0.188 | [-0.337, -0.043] | -0.067 | FAILED_OOS |
| zone_rejection | 6 | -0.58 | [-1.311, 1.309] | -0.343 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 66 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 66, 'mean_difference_R': 0.037, 'ci_low': -0.217, 'ci_high': 0.272, 'atr_exp_R': -0.487, 'chart_exp_R': -0.45}

Baseline (1h trend, one trade a day) OOS: {'trades': 62, 'win_rate': 0.435, 'avg_win_R': 1.329, 'avg_loss_R': -1.278, 'gross_expectancy_R': 0.238, 'net_expectancy_R': -0.143, 'cost_per_trade_R': 0.381, 'total_net_R': -8.86, 'profit_factor': 0.8, 'max_drawdown_R': 16.51, 'longest_losing_streak': 6, 't_stat': -0.8, 'ci_level': 0.9996, 'ci_low': -0.66, 'ci_high': 0.431}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.