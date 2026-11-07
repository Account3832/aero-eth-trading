# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for BNB-USD. Long-only. Paper only.**

Data: BNB-USD 2025-10-22 18:45:00+00:00 to 2026-11-07 03:45:00+00:00 (382 days). Generated 2026-11-07 04:05:48.213213+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 103 | -0.854 | [-1.259, -0.324] | -0.051 | FAILED_OOS |
| donchian_breakout | 42 | -0.714 | [-1.325, -0.113] | -0.065 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 22 | -0.911 | [-1.808, 0.139] | -0.023 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 15 | -0.857 | [-1.593, -0.029] | -0.06 | INSUFFICIENT_SAMPLE |
| range_bounce | 50 | -1.191 | [-1.669, -0.694] | -0.06 | INSUFFICIENT_SAMPLE |
| btc_lead | 10 | -0.93 | [-2.27, 0.334] | -0.023 | INSUFFICIENT_SAMPLE |
| support_bounce | 30 | -1.07 | [-1.821, -0.22] | -0.068 | INSUFFICIENT_SAMPLE |
| swing_breakout | 38 | -0.558 | [-1.286, 0.204] | -0.023 | INSUFFICIENT_SAMPLE |
| steady_scalper | 115 | -0.632 | [-0.857, -0.413] | -0.081 | FAILED_OOS |
| zone_rejection | 2 | 0.505 | [-0.453, 1.463] | 0.474 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 50 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 50, 'mean_difference_R': -0.048, 'ci_low': -0.269, 'ci_high': 0.155, 'atr_exp_R': -0.751, 'chart_exp_R': -0.799}

Baseline (1h trend, one trade a day) OOS: {'trades': 37, 'win_rate': 0.297, 'avg_win_R': 0.912, 'avg_loss_R': -1.694, 'gross_expectancy_R': -0.036, 'net_expectancy_R': -0.919, 'cost_per_trade_R': 0.883, 'total_net_R': -34.0, 'profit_factor': 0.23, 'max_drawdown_R': 31.93, 'longest_losing_streak': 8, 't_stat': -4.12, 'ci_level': 0.9996, 'ci_low': -1.659, 'ci_high': -0.023}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.