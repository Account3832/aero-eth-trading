# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for XRP-USD. Long-only. Paper only.**

Data: XRP-USD 2024-10-20 00:00:00+00:00 to 2026-11-28 11:30:00+00:00 (770 days). Generated 2026-11-28 11:54:51.808683+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 179 | -0.544 | [-0.835, -0.189] | -0.063 | FAILED_OOS |
| donchian_breakout | 84 | -0.286 | [-0.781, 0.241] | -0.016 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 38 | -0.488 | [-1.337, 0.545] | -0.009 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 22 | -0.452 | [-1.119, 0.273] | -0.042 | INSUFFICIENT_SAMPLE |
| range_bounce | 106 | -0.774 | [-1.123, -0.43] | -0.046 | FAILED_OOS |
| btc_lead | 5 | -0.834 | [-2.533, 0.485] | -0.011 | INSUFFICIENT_SAMPLE |
| support_bounce | 47 | -0.25 | [-0.916, 0.393] | 0.041 | INSUFFICIENT_SAMPLE |
| swing_breakout | 89 | -0.371 | [-0.751, 0.147] | -0.035 | INSUFFICIENT_SAMPLE |
| steady_scalper | 202 | -0.344 | [-0.478, -0.178] | -0.072 | FAILED_OOS |
| zone_rejection | 6 | -1.275 | [-1.401, -1.135] | -0.48 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 58 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 58, 'mean_difference_R': 0.06, 'ci_low': -0.132, 'ci_high': 0.269, 'atr_exp_R': -0.527, 'chart_exp_R': -0.467}

Baseline (1h trend, one trade a day) OOS: {'trades': 57, 'win_rate': 0.456, 'avg_win_R': 1.148, 'avg_loss_R': -1.39, 'gross_expectancy_R': 0.326, 'net_expectancy_R': -0.232, 'cost_per_trade_R': 0.558, 'total_net_R': -13.24, 'profit_factor': 0.69, 'max_drawdown_R': 15.3, 'longest_losing_streak': 7, 't_stat': -1.26, 'ci_level': 0.9996, 'ci_low': -0.825, 'ci_high': 0.439}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.