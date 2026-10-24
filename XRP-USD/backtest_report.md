# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for XRP-USD. Long-only. Paper only.**

Data: XRP-USD 2024-10-20 00:00:00+00:00 to 2026-10-24 03:30:00+00:00 (735 days). Generated 2026-10-24 03:50:24.233587+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 185 | -0.609 | [-0.962, -0.235] | -0.068 | FAILED_OOS |
| donchian_breakout | 89 | -0.273 | [-0.728, 0.22] | -0.004 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 40 | -0.569 | [-1.279, 0.423] | -0.021 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 22 | -0.398 | [-0.979, 0.238] | -0.014 | INSUFFICIENT_SAMPLE |
| range_bounce | 92 | -0.957 | [-1.361, -0.599] | -0.065 | INSUFFICIENT_SAMPLE |
| btc_lead | 5 | -0.519 | [-2.218, 0.485] | 0.031 | INSUFFICIENT_SAMPLE |
| support_bounce | 46 | -0.456 | [-1.052, 0.187] | 0.002 | INSUFFICIENT_SAMPLE |
| swing_breakout | 94 | -0.213 | [-0.696, 0.314] | 0.029 | INSUFFICIENT_SAMPLE |
| steady_scalper | 209 | -0.375 | [-0.529, -0.189] | -0.072 | FAILED_OOS |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 62 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 62, 'mean_difference_R': -0.027, 'ci_low': -0.234, 'ci_high': 0.185, 'atr_exp_R': -0.607, 'chart_exp_R': -0.634}

Baseline (1h trend, one trade a day) OOS: {'trades': 57, 'win_rate': 0.491, 'avg_win_R': 1.031, 'avg_loss_R': -1.463, 'gross_expectancy_R': 0.386, 'net_expectancy_R': -0.238, 'cost_per_trade_R': 0.624, 'total_net_R': -13.57, 'profit_factor': 0.68, 'max_drawdown_R': 13.81, 'longest_losing_streak': 5, 't_stat': -1.29, 'ci_level': 0.9995, 'ci_low': -0.804, 'ci_high': 0.412}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.