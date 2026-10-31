# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for SOL-USD. Long-only. Paper only.**

Data: SOL-USD 2024-10-20 00:00:00+00:00 to 2026-10-31 03:30:00+00:00 (742 days). Generated 2026-10-31 03:59:01.632684+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 215 | -0.571 | [-0.88, -0.303] | -0.055 | FAILED_OOS |
| donchian_breakout | 89 | -0.334 | [-0.751, 0.104] | -0.025 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 58 | -0.632 | [-1.19, 0.113] | -0.038 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 37 | -0.674 | [-1.117, -0.19] | -0.114 | INSUFFICIENT_SAMPLE |
| range_bounce | 81 | -0.765 | [-1.111, -0.411] | -0.056 | INSUFFICIENT_SAMPLE |
| btc_lead | 8 | -0.981 | [-2.007, 0.106] | -0.121 | INSUFFICIENT_SAMPLE |
| support_bounce | 52 | -0.642 | [-1.187, 0.045] | -0.056 | INSUFFICIENT_SAMPLE |
| swing_breakout | 85 | -0.365 | [-0.758, 0.183] | -0.031 | INSUFFICIENT_SAMPLE |
| steady_scalper | 241 | -0.417 | [-0.554, -0.265] | -0.088 | FAILED_OOS |
| zone_rejection | 3 | -0.437 | [-1.253, 0.894] | -0.089 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 72 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 72, 'mean_difference_R': 0.103, 'ci_low': -0.128, 'ci_high': 0.321, 'atr_exp_R': -0.682, 'chart_exp_R': -0.579}

Baseline (1h trend, one trade a day) OOS: {'trades': 73, 'win_rate': 0.397, 'avg_win_R': 0.939, 'avg_loss_R': -1.503, 'gross_expectancy_R': 0.076, 'net_expectancy_R': -0.533, 'cost_per_trade_R': 0.609, 'total_net_R': -38.87, 'profit_factor': 0.41, 'max_drawdown_R': 38.86, 'longest_losing_streak': 8, 't_stat': -3.48, 'ci_level': 0.9996, 'ci_low': -1.025, 'ci_high': -0.01}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.