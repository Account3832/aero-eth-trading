# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for DOGE-USD. Long-only. Paper only.**

Data: DOGE-USD 2024-10-20 00:00:00+00:00 to 2026-10-31 03:30:00+00:00 (742 days). Generated 2026-10-31 03:59:15.336219+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 168 | -0.543 | [-0.821, -0.179] | -0.069 | FAILED_OOS |
| donchian_breakout | 74 | -0.359 | [-0.833, 0.119] | -0.042 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 41 | -0.528 | [-1.182, 0.193] | -0.022 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 30 | -0.232 | [-0.93, 0.33] | 0.023 | INSUFFICIENT_SAMPLE |
| range_bounce | 82 | -0.863 | [-1.245, -0.51] | -0.079 | INSUFFICIENT_SAMPLE |
| btc_lead | 7 | -0.405 | [-1.254, 0.685] | 0.0 | INSUFFICIENT_SAMPLE |
| support_bounce | 67 | -0.863 | [-1.267, -0.35] | -0.115 | INSUFFICIENT_SAMPLE |
| swing_breakout | 78 | -0.393 | [-0.805, 0.091] | -0.039 | INSUFFICIENT_SAMPLE |
| steady_scalper | 186 | -0.361 | [-0.515, -0.229] | -0.085 | FAILED_OOS |
| zone_rejection | 6 | -0.019 | [-1.483, 2.76] | 0.093 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 53 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 53, 'mean_difference_R': 0.087, 'ci_low': -0.158, 'ci_high': 0.334, 'atr_exp_R': -0.61, 'chart_exp_R': -0.523}

Baseline (1h trend, one trade a day) OOS: {'trades': 58, 'win_rate': 0.5, 'avg_win_R': 0.935, 'avg_loss_R': -1.467, 'gross_expectancy_R': 0.309, 'net_expectancy_R': -0.266, 'cost_per_trade_R': 0.575, 'total_net_R': -15.45, 'profit_factor': 0.64, 'max_drawdown_R': 14.26, 'longest_losing_streak': 3, 't_stat': -1.54, 'ci_level': 0.9996, 'ci_low': -0.855, 'ci_high': 0.303}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.