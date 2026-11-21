# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for LTC-USD. Long-only. Paper only.**

Data: LTC-USD 2024-10-20 00:00:00+00:00 to 2026-11-21 10:45:00+00:00 (763 days). Generated 2026-11-21 11:15:52.308269+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 169 | -0.582 | [-0.87, -0.217] | -0.063 | FAILED_OOS |
| donchian_breakout | 54 | -0.498 | [-1.026, 0.064] | -0.085 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 30 | -0.587 | [-1.303, 0.232] | -0.03 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 10 | -0.25 | [-1.393, 0.907] | 0.029 | INSUFFICIENT_SAMPLE |
| range_bounce | 97 | -0.711 | [-1.043, -0.32] | -0.045 | INSUFFICIENT_SAMPLE |
| btc_lead | 13 | -0.581 | [-1.42, 0.478] | -0.032 | INSUFFICIENT_SAMPLE |
| support_bounce | 60 | -0.581 | [-1.152, 0.066] | -0.035 | INSUFFICIENT_SAMPLE |
| swing_breakout | 79 | -0.522 | [-0.916, -0.058] | -0.1 | INSUFFICIENT_SAMPLE |
| steady_scalper | 196 | -0.405 | [-0.556, -0.231] | -0.086 | FAILED_OOS |
| zone_rejection | 6 | -0.587 | [-1.637, 1.251] | -0.076 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 65 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 65, 'mean_difference_R': 0.097, 'ci_low': -0.181, 'ci_high': 0.381, 'atr_exp_R': -0.328, 'chart_exp_R': -0.231}

Baseline (1h trend, one trade a day) OOS: {'trades': 62, 'win_rate': 0.387, 'avg_win_R': 1.249, 'avg_loss_R': -1.51, 'gross_expectancy_R': 0.167, 'net_expectancy_R': -0.442, 'cost_per_trade_R': 0.609, 'total_net_R': -27.42, 'profit_factor': 0.52, 'max_drawdown_R': 25.95, 'longest_losing_streak': 5, 't_stat': -2.38, 'ci_level': 0.9996, 'ci_low': -1.001, 'ci_high': 0.284}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.