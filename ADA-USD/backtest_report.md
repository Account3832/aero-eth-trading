# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for ADA-USD. Long-only. Paper only.**

Data: ADA-USD 2024-10-20 00:00:00+00:00 to 2026-10-24 03:30:00+00:00 (735 days). Generated 2026-10-24 03:50:50.111249+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 172 | -0.337 | [-0.651, 0.001] | -0.038 | NOT_DEMONSTRATED |
| donchian_breakout | 80 | -0.341 | [-0.757, 0.175] | -0.09 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 34 | -0.765 | [-1.251, -0.07] | -0.152 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 15 | -0.527 | [-1.272, 0.442] | -0.123 | INSUFFICIENT_SAMPLE |
| range_bounce | 83 | -0.635 | [-0.996, -0.244] | -0.081 | INSUFFICIENT_SAMPLE |
| btc_lead | 9 | -0.35 | [-1.373, 0.856] | -0.001 | INSUFFICIENT_SAMPLE |
| support_bounce | 45 | -0.643 | [-1.189, 0.116] | -0.102 | INSUFFICIENT_SAMPLE |
| swing_breakout | 98 | -0.503 | [-0.858, -0.076] | -0.161 | INSUFFICIENT_SAMPLE |
| steady_scalper | 199 | -0.256 | [-0.414, -0.094] | -0.071 | FAILED_OOS |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 77 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 77, 'mean_difference_R': 0.157, 'ci_low': -0.032, 'ci_high': 0.379, 'atr_exp_R': -0.267, 'chart_exp_R': -0.111}

Baseline (1h trend, one trade a day) OOS: {'trades': 63, 'win_rate': 0.444, 'avg_win_R': 1.105, 'avg_loss_R': -1.386, 'gross_expectancy_R': 0.159, 'net_expectancy_R': -0.279, 'cost_per_trade_R': 0.438, 'total_net_R': -17.56, 'profit_factor': 0.64, 'max_drawdown_R': 16.61, 'longest_losing_streak': 5, 't_stat': -1.65, 'ci_level': 0.9995, 'ci_low': -0.802, 'ci_high': 0.255}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.