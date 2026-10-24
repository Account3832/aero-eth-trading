# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for LINK-USD. Long-only. Paper only.**

Data: LINK-USD 2024-10-20 00:00:00+00:00 to 2026-10-24 03:30:00+00:00 (735 days). Generated 2026-10-24 03:50:57.382941+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 217 | -0.577 | [-0.836, -0.262] | -0.068 | FAILED_OOS |
| donchian_breakout | 81 | -0.165 | [-0.67, 0.396] | 0.031 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 52 | -0.932 | [-1.393, -0.43] | -0.111 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 27 | -0.512 | [-1.182, 0.209] | -0.066 | INSUFFICIENT_SAMPLE |
| range_bounce | 81 | -0.73 | [-1.092, -0.35] | -0.063 | INSUFFICIENT_SAMPLE |
| btc_lead | 3 | 0.001 | [-1.332, 1.075] | 0.1 | INSUFFICIENT_SAMPLE |
| support_bounce | 51 | -0.55 | [-1.093, 0.045] | -0.049 | INSUFFICIENT_SAMPLE |
| swing_breakout | 100 | -0.21 | [-0.656, 0.269] | 0.02 | NOT_DEMONSTRATED |
| steady_scalper | 249 | -0.425 | [-0.559, -0.289] | -0.108 | FAILED_OOS |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 73 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 73, 'mean_difference_R': 0.097, 'ci_low': -0.127, 'ci_high': 0.322, 'atr_exp_R': -0.277, 'chart_exp_R': -0.18}

Baseline (1h trend, one trade a day) OOS: {'trades': 73, 'win_rate': 0.329, 'avg_win_R': 1.033, 'avg_loss_R': -1.44, 'gross_expectancy_R': -0.081, 'net_expectancy_R': -0.627, 'cost_per_trade_R': 0.546, 'total_net_R': -45.79, 'profit_factor': 0.35, 'max_drawdown_R': 44.51, 'longest_losing_streak': 8, 't_stat': -4.23, 'ci_level': 0.9995, 'ci_low': -1.08, 'ci_high': -0.142}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.