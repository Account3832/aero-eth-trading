# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for SOL-USD. Long-only. Paper only.**

Data: SOL-USD 2024-10-20 00:00:00+00:00 to 2026-11-07 03:45:00+00:00 (749 days). Generated 2026-11-07 04:06:19.083789+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 209 | -0.563 | [-0.792, -0.255] | -0.058 | FAILED_OOS |
| donchian_breakout | 86 | -0.29 | [-0.682, 0.103] | -0.013 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 54 | -0.543 | [-1.087, 0.072] | -0.026 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 38 | -0.694 | [-1.115, -0.23] | -0.12 | INSUFFICIENT_SAMPLE |
| range_bounce | 85 | -0.801 | [-1.162, -0.362] | -0.062 | INSUFFICIENT_SAMPLE |
| btc_lead | 7 | -0.899 | [-2.043, 0.176] | -0.103 | INSUFFICIENT_SAMPLE |
| support_bounce | 51 | -0.719 | [-1.243, 0.036] | -0.078 | INSUFFICIENT_SAMPLE |
| swing_breakout | 83 | -0.312 | [-0.735, 0.078] | -0.018 | INSUFFICIENT_SAMPLE |
| steady_scalper | 233 | -0.415 | [-0.578, -0.277] | -0.093 | FAILED_OOS |
| zone_rejection | 3 | -0.437 | [-1.253, 0.894] | -0.089 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 72 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 72, 'mean_difference_R': 0.103, 'ci_low': -0.128, 'ci_high': 0.321, 'atr_exp_R': -0.682, 'chart_exp_R': -0.579}

Baseline (1h trend, one trade a day) OOS: {'trades': 71, 'win_rate': 0.394, 'avg_win_R': 0.97, 'avg_loss_R': -1.533, 'gross_expectancy_R': 0.052, 'net_expectancy_R': -0.546, 'cost_per_trade_R': 0.598, 'total_net_R': -38.74, 'profit_factor': 0.41, 'max_drawdown_R': 40.36, 'longest_losing_streak': 8, 't_stat': -3.48, 'ci_level': 0.9996, 'ci_low': -0.983, 'ci_high': -0.012}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.