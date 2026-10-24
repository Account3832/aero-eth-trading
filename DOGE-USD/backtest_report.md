# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for DOGE-USD. Long-only. Paper only.**

Data: DOGE-USD 2024-10-20 00:00:00+00:00 to 2026-10-24 03:30:00+00:00 (735 days). Generated 2026-10-24 03:50:42.622610+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 169 | -0.583 | [-0.882, -0.29] | -0.079 | FAILED_OOS |
| donchian_breakout | 74 | -0.405 | [-0.827, 0.17] | -0.058 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 42 | -0.605 | [-1.239, 0.017] | -0.038 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 28 | -0.214 | [-0.883, 0.403] | 0.03 | INSUFFICIENT_SAMPLE |
| range_bounce | 83 | -0.874 | [-1.23, -0.469] | -0.08 | INSUFFICIENT_SAMPLE |
| btc_lead | 7 | -0.405 | [-1.253, 0.675] | 0.0 | INSUFFICIENT_SAMPLE |
| support_bounce | 66 | -0.828 | [-1.274, -0.309] | -0.106 | INSUFFICIENT_SAMPLE |
| swing_breakout | 77 | -0.43 | [-0.897, 0.053] | -0.05 | INSUFFICIENT_SAMPLE |
| steady_scalper | 184 | -0.365 | [-0.524, -0.21] | -0.086 | FAILED_OOS |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 54 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 54, 'mean_difference_R': 0.087, 'ci_low': -0.164, 'ci_high': 0.344, 'atr_exp_R': -0.623, 'chart_exp_R': -0.536}

Baseline (1h trend, one trade a day) OOS: {'trades': 59, 'win_rate': 0.492, 'avg_win_R': 0.935, 'avg_loss_R': -1.474, 'gross_expectancy_R': 0.289, 'net_expectancy_R': -0.29, 'cost_per_trade_R': 0.579, 'total_net_R': -17.11, 'profit_factor': 0.61, 'max_drawdown_R': 15.66, 'longest_losing_streak': 4, 't_stat': -1.69, 'ci_level': 0.9995, 'ci_low': -0.89, 'ci_high': 0.364}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.