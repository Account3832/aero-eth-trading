# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for AERO-USD. Long-only. Paper only.**

Data: AERO-USD 2024-10-18 00:00:00+00:00 to 2026-11-07 03:45:00+00:00 (751 days). Generated 2026-11-07 04:05:15.731435+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.1% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 207 | -0.238 | [-0.57, 0.105] | -0.024 | NOT_DEMONSTRATED |
| donchian_breakout | 88 | -0.364 | [-0.741, 0.146] | -0.164 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 39 | -0.558 | [-1.079, 0.117] | -0.118 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 24 | -0.539 | [-1.198, 0.184] | -0.152 | INSUFFICIENT_SAMPLE |
| range_bounce | 88 | -0.628 | [-0.998, -0.241] | -0.104 | INSUFFICIENT_SAMPLE |
| btc_lead | 8 | -0.609 | [-1.405, 0.585] | -0.221 | INSUFFICIENT_SAMPLE |
| support_bounce | 52 | -0.044 | [-0.614, 0.576] | 0.079 | INSUFFICIENT_SAMPLE |
| swing_breakout | 99 | -0.152 | [-0.577, 0.285] | -0.001 | INSUFFICIENT_SAMPLE |
| steady_scalper | 227 | -0.192 | [-0.357, -0.054] | -0.07 | FAILED_OOS |
| zone_rejection | 6 | -0.58 | [-1.311, 1.309] | -0.343 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 68 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 68, 'mean_difference_R': 0.038, 'ci_low': -0.204, 'ci_high': 0.266, 'atr_exp_R': -0.511, 'chart_exp_R': -0.473}

Baseline (1h trend, one trade a day) OOS: {'trades': 64, 'win_rate': 0.422, 'avg_win_R': 1.329, 'avg_loss_R': -1.284, 'gross_expectancy_R': 0.203, 'net_expectancy_R': -0.182, 'cost_per_trade_R': 0.385, 'total_net_R': -11.63, 'profit_factor': 0.76, 'max_drawdown_R': 16.51, 'longest_losing_streak': 6, 't_stat': -1.04, 'ci_level': 0.9996, 'ci_low': -0.648, 'ci_high': 0.439}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.