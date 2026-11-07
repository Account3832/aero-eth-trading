# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for XRP-USD. Long-only. Paper only.**

Data: XRP-USD 2024-10-20 00:00:00+00:00 to 2026-11-07 03:45:00+00:00 (749 days). Generated 2026-11-07 04:06:01.043328+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 188 | -0.551 | [-0.827, -0.225] | -0.06 | FAILED_OOS |
| donchian_breakout | 87 | -0.242 | [-0.757, 0.26] | 0.006 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 38 | -0.461 | [-1.246, 0.277] | 0.0 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 24 | -0.478 | [-1.133, 0.212] | -0.039 | INSUFFICIENT_SAMPLE |
| range_bounce | 95 | -0.906 | [-1.238, -0.542] | -0.059 | INSUFFICIENT_SAMPLE |
| btc_lead | 5 | -0.834 | [-2.533, 0.485] | -0.011 | INSUFFICIENT_SAMPLE |
| support_bounce | 45 | -0.366 | [-1.004, 0.321] | 0.018 | INSUFFICIENT_SAMPLE |
| swing_breakout | 93 | -0.247 | [-0.733, 0.19] | 0.014 | INSUFFICIENT_SAMPLE |
| steady_scalper | 214 | -0.351 | [-0.506, -0.209] | -0.069 | FAILED_OOS |
| zone_rejection | 7 | -1.049 | [-1.398, -0.228] | -0.368 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 60 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 60, 'mean_difference_R': -0.043, 'ci_low': -0.26, 'ci_high': 0.182, 'atr_exp_R': -0.545, 'chart_exp_R': -0.588}

Baseline (1h trend, one trade a day) OOS: {'trades': 57, 'win_rate': 0.509, 'avg_win_R': 1.098, 'avg_loss_R': -1.409, 'gross_expectancy_R': 0.449, 'net_expectancy_R': -0.134, 'cost_per_trade_R': 0.583, 'total_net_R': -7.61, 'profit_factor': 0.81, 'max_drawdown_R': 10.71, 'longest_losing_streak': 5, 't_stat': -0.72, 'ci_level': 0.9996, 'ci_low': -0.767, 'ci_high': 0.413}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.