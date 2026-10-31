# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for XRP-USD. Long-only. Paper only.**

Data: XRP-USD 2024-10-20 00:00:00+00:00 to 2026-10-31 03:30:00+00:00 (742 days). Generated 2026-10-31 03:58:50.693054+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 187 | -0.602 | [-0.903, -0.263] | -0.067 | FAILED_OOS |
| donchian_breakout | 87 | -0.247 | [-0.743, 0.265] | 0.006 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 40 | -0.524 | [-1.294, 0.33] | -0.012 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 23 | -0.44 | [-1.041, 0.231] | -0.027 | INSUFFICIENT_SAMPLE |
| range_bounce | 92 | -0.944 | [-1.259, -0.598] | -0.066 | INSUFFICIENT_SAMPLE |
| btc_lead | 5 | -0.519 | [-2.218, 0.485] | 0.031 | INSUFFICIENT_SAMPLE |
| support_bounce | 45 | -0.434 | [-1.043, 0.225] | 0.007 | INSUFFICIENT_SAMPLE |
| swing_breakout | 93 | -0.199 | [-0.725, 0.334] | 0.033 | INSUFFICIENT_SAMPLE |
| steady_scalper | 213 | -0.37 | [-0.503, -0.23] | -0.071 | FAILED_OOS |
| zone_rejection | 7 | -1.049 | [-1.398, -0.228] | -0.368 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 61 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 61, 'mean_difference_R': -0.04, 'ci_low': -0.251, 'ci_high': 0.183, 'atr_exp_R': -0.564, 'chart_exp_R': -0.603}

Baseline (1h trend, one trade a day) OOS: {'trades': 56, 'win_rate': 0.518, 'avg_win_R': 1.059, 'avg_loss_R': -1.427, 'gross_expectancy_R': 0.464, 'net_expectancy_R': -0.14, 'cost_per_trade_R': 0.603, 'total_net_R': -7.81, 'profit_factor': 0.8, 'max_drawdown_R': 12.12, 'longest_losing_streak': 5, 't_stat': -0.75, 'ci_level': 0.9996, 'ci_low': -0.634, 'ci_high': 0.456}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.