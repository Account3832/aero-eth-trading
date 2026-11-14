# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for LTC-USD. Long-only. Paper only.**

Data: LTC-USD 2024-10-20 00:00:00+00:00 to 2026-11-14 10:15:00+00:00 (756 days). Generated 2026-11-14 10:36:12.251320+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 176 | -0.568 | [-0.857, -0.235] | -0.059 | FAILED_OOS |
| donchian_breakout | 57 | -0.478 | [-1.031, 0.096] | -0.079 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 30 | -0.587 | [-1.303, 0.232] | -0.03 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 13 | -0.066 | [-1.035, 0.91] | 0.082 | INSUFFICIENT_SAMPLE |
| range_bounce | 96 | -0.723 | [-1.123, -0.325] | -0.046 | INSUFFICIENT_SAMPLE |
| btc_lead | 13 | -0.581 | [-1.42, 0.478] | -0.032 | INSUFFICIENT_SAMPLE |
| support_bounce | 60 | -0.528 | [-1.184, 0.091] | -0.022 | INSUFFICIENT_SAMPLE |
| swing_breakout | 78 | -0.493 | [-0.927, -0.075] | -0.086 | INSUFFICIENT_SAMPLE |
| steady_scalper | 206 | -0.403 | [-0.56, -0.224] | -0.085 | FAILED_OOS |
| zone_rejection | 8 | -0.18 | [-1.502, 1.884] | 0.046 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 66 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 66, 'mean_difference_R': 0.111, 'ci_low': -0.169, 'ci_high': 0.415, 'atr_exp_R': -0.297, 'chart_exp_R': -0.186}

Baseline (1h trend, one trade a day) OOS: {'trades': 63, 'win_rate': 0.397, 'avg_win_R': 1.268, 'avg_loss_R': -1.51, 'gross_expectancy_R': 0.202, 'net_expectancy_R': -0.408, 'cost_per_trade_R': 0.61, 'total_net_R': -25.7, 'profit_factor': 0.55, 'max_drawdown_R': 27.42, 'longest_losing_streak': 5, 't_stat': -2.19, 'ci_level': 0.9996, 'ci_low': -0.968, 'ci_high': 0.169}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.