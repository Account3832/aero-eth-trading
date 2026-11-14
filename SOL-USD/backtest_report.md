# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for SOL-USD. Long-only. Paper only.**

Data: SOL-USD 2024-10-20 00:00:00+00:00 to 2026-11-14 10:15:00+00:00 (756 days). Generated 2026-11-14 10:34:46.465230+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 197 | -0.586 | [-0.912, -0.302] | -0.066 | FAILED_OOS |
| donchian_breakout | 78 | -0.261 | [-0.69, 0.277] | -0.003 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 54 | -0.543 | [-1.087, 0.072] | -0.026 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 37 | -0.731 | [-1.131, -0.254] | -0.131 | INSUFFICIENT_SAMPLE |
| range_bounce | 89 | -0.803 | [-1.155, -0.448] | -0.062 | INSUFFICIENT_SAMPLE |
| btc_lead | 7 | -0.899 | [-2.043, 0.176] | -0.103 | INSUFFICIENT_SAMPLE |
| support_bounce | 50 | -0.701 | [-1.281, -0.109] | -0.074 | INSUFFICIENT_SAMPLE |
| swing_breakout | 81 | -0.311 | [-0.802, 0.197] | -0.018 | INSUFFICIENT_SAMPLE |
| steady_scalper | 219 | -0.442 | [-0.612, -0.309] | -0.107 | FAILED_OOS |
| zone_rejection | 3 | -0.437 | [-1.253, 0.894] | -0.089 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 68 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 68, 'mean_difference_R': 0.114, 'ci_low': -0.131, 'ci_high': 0.346, 'atr_exp_R': -0.712, 'chart_exp_R': -0.598}

Baseline (1h trend, one trade a day) OOS: {'trades': 66, 'win_rate': 0.409, 'avg_win_R': 0.946, 'avg_loss_R': -1.526, 'gross_expectancy_R': 0.073, 'net_expectancy_R': -0.515, 'cost_per_trade_R': 0.588, 'total_net_R': -33.96, 'profit_factor': 0.43, 'max_drawdown_R': 32.45, 'longest_losing_streak': 4, 't_stat': -3.17, 'ci_level': 0.9996, 'ci_low': -1.024, 'ci_high': 0.045}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.