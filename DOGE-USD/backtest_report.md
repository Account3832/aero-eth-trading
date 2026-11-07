# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for DOGE-USD. Long-only. Paper only.**

Data: DOGE-USD 2024-10-20 00:00:00+00:00 to 2026-11-07 03:45:00+00:00 (749 days). Generated 2026-11-07 04:06:42.136694+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 168 | -0.525 | [-0.847, -0.187] | -0.064 | FAILED_OOS |
| donchian_breakout | 71 | -0.358 | [-0.792, 0.243] | -0.041 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 37 | -0.476 | [-1.16, 0.288] | -0.011 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 32 | -0.255 | [-0.777, 0.31] | 0.015 | INSUFFICIENT_SAMPLE |
| range_bounce | 83 | -0.841 | [-1.175, -0.367] | -0.073 | INSUFFICIENT_SAMPLE |
| btc_lead | 7 | -0.685 | [-1.698, 0.582] | -0.051 | INSUFFICIENT_SAMPLE |
| support_bounce | 67 | -0.851 | [-1.291, -0.361] | -0.111 | INSUFFICIENT_SAMPLE |
| swing_breakout | 80 | -0.417 | [-0.859, 0.061] | -0.046 | INSUFFICIENT_SAMPLE |
| steady_scalper | 185 | -0.358 | [-0.514, -0.182] | -0.084 | FAILED_OOS |
| zone_rejection | 5 | 0.251 | [-1.474, 2.987] | 0.2 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 52 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 52, 'mean_difference_R': 0.067, 'ci_low': -0.205, 'ci_high': 0.344, 'atr_exp_R': -0.487, 'chart_exp_R': -0.42}

Baseline (1h trend, one trade a day) OOS: {'trades': 56, 'win_rate': 0.5, 'avg_win_R': 0.954, 'avg_loss_R': -1.484, 'gross_expectancy_R': 0.323, 'net_expectancy_R': -0.265, 'cost_per_trade_R': 0.587, 'total_net_R': -14.83, 'profit_factor': 0.64, 'max_drawdown_R': 15.1, 'longest_losing_streak': 4, 't_stat': -1.49, 'ci_level': 0.9996, 'ci_low': -0.784, 'ci_high': 0.36}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.