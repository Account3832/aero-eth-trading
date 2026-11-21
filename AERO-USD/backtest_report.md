# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for AERO-USD. Long-only. Paper only.**

Data: AERO-USD 2024-10-18 00:00:00+00:00 to 2026-11-21 10:45:00+00:00 (765 days). Generated 2026-11-21 11:13:26.983868+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.1% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 194 | -0.25 | [-0.568, 0.067] | -0.029 | NOT_DEMONSTRATED |
| donchian_breakout | 81 | -0.373 | [-0.792, 0.177] | -0.175 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 39 | -0.558 | [-1.079, 0.117] | -0.118 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 20 | -0.39 | [-1.146, 0.53] | -0.078 | INSUFFICIENT_SAMPLE |
| range_bounce | 98 | -0.64 | [-1.028, -0.253] | -0.105 | INSUFFICIENT_SAMPLE |
| btc_lead | 7 | -0.514 | [-1.4, 1.088] | -0.193 | INSUFFICIENT_SAMPLE |
| support_bounce | 52 | -0.179 | [-0.767, 0.4] | 0.015 | INSUFFICIENT_SAMPLE |
| swing_breakout | 92 | -0.145 | [-0.573, 0.374] | 0.003 | INSUFFICIENT_SAMPLE |
| steady_scalper | 211 | -0.198 | [-0.346, -0.06] | -0.074 | FAILED_OOS |
| zone_rejection | 6 | -0.58 | [-1.311, 1.309] | -0.343 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 64 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 64, 'mean_difference_R': 0.037, 'ci_low': -0.223, 'ci_high': 0.274, 'atr_exp_R': -0.466, 'chart_exp_R': -0.43}

Baseline (1h trend, one trade a day) OOS: {'trades': 59, 'win_rate': 0.441, 'avg_win_R': 1.3, 'avg_loss_R': -1.282, 'gross_expectancy_R': 0.242, 'net_expectancy_R': -0.144, 'cost_per_trade_R': 0.386, 'total_net_R': -8.51, 'profit_factor': 0.8, 'max_drawdown_R': 16.51, 'longest_losing_streak': 6, 't_stat': -0.79, 'ci_level': 0.9996, 'ci_low': -0.668, 'ci_high': 0.464}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.