# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for LINK-USD. Long-only. Paper only.**

Data: LINK-USD 2024-10-20 00:00:00+00:00 to 2026-11-07 03:45:00+00:00 (749 days). Generated 2026-11-07 04:07:16.716113+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 212 | -0.508 | [-0.773, -0.197] | -0.055 | FAILED_OOS |
| donchian_breakout | 83 | -0.106 | [-0.642, 0.405] | 0.055 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 49 | -0.87 | [-1.333, -0.312] | -0.106 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 30 | -0.481 | [-1.095, 0.148] | -0.061 | INSUFFICIENT_SAMPLE |
| range_bounce | 81 | -0.735 | [-1.09, -0.332] | -0.071 | INSUFFICIENT_SAMPLE |
| btc_lead | 3 | 0.001 | [-1.332, 1.075] | 0.1 | INSUFFICIENT_SAMPLE |
| support_bounce | 53 | -0.5 | [-0.995, 0.187] | -0.043 | INSUFFICIENT_SAMPLE |
| swing_breakout | 99 | -0.163 | [-0.641, 0.283] | 0.036 | INSUFFICIENT_SAMPLE |
| steady_scalper | 244 | -0.385 | [-0.513, -0.235] | -0.096 | FAILED_OOS |
| zone_rejection | 8 | 0.312 | [-1.343, 1.968] | 0.227 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 72 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 72, 'mean_difference_R': 0.1, 'ci_low': -0.118, 'ci_high': 0.333, 'atr_exp_R': -0.263, 'chart_exp_R': -0.164}

Baseline (1h trend, one trade a day) OOS: {'trades': 74, 'win_rate': 0.338, 'avg_win_R': 1.005, 'avg_loss_R': -1.418, 'gross_expectancy_R': -0.071, 'net_expectancy_R': -0.599, 'cost_per_trade_R': 0.528, 'total_net_R': -44.34, 'profit_factor': 0.36, 'max_drawdown_R': 44.54, 'longest_losing_streak': 8, 't_stat': -4.12, 'ci_level': 0.9996, 'ci_low': -1.057, 'ci_high': -0.088}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.