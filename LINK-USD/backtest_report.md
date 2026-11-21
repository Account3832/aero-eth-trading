# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for LINK-USD. Long-only. Paper only.**

Data: LINK-USD 2024-10-20 00:00:00+00:00 to 2026-11-21 10:45:00+00:00 (763 days). Generated 2026-11-21 11:15:27.007884+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 193 | -0.549 | [-0.856, -0.27] | -0.068 | FAILED_OOS |
| donchian_breakout | 74 | -0.253 | [-0.689, 0.311] | -0.008 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 49 | -0.87 | [-1.333, -0.312] | -0.106 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 26 | -0.506 | [-1.086, 0.162] | -0.075 | INSUFFICIENT_SAMPLE |
| range_bounce | 94 | -0.606 | [-0.954, -0.281] | -0.044 | INSUFFICIENT_SAMPLE |
| btc_lead | 3 | 0.001 | [-1.332, 1.075] | 0.1 | INSUFFICIENT_SAMPLE |
| support_bounce | 53 | -0.504 | [-1.076, 0.096] | -0.043 | INSUFFICIENT_SAMPLE |
| swing_breakout | 91 | -0.328 | [-0.714, 0.128] | -0.03 | INSUFFICIENT_SAMPLE |
| steady_scalper | 222 | -0.424 | [-0.569, -0.266] | -0.117 | FAILED_OOS |
| zone_rejection | 6 | -0.192 | [-1.405, 1.805] | 0.018 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 62 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 62, 'mean_difference_R': -0.001, 'ci_low': -0.236, 'ci_high': 0.244, 'atr_exp_R': -0.274, 'chart_exp_R': -0.274}

Baseline (1h trend, one trade a day) OOS: {'trades': 67, 'win_rate': 0.343, 'avg_win_R': 1.003, 'avg_loss_R': -1.414, 'gross_expectancy_R': -0.053, 'net_expectancy_R': -0.585, 'cost_per_trade_R': 0.531, 'total_net_R': -39.17, 'profit_factor': 0.37, 'max_drawdown_R': 40.95, 'longest_losing_streak': 8, 't_stat': -3.82, 'ci_level': 0.9996, 'ci_low': -1.015, 'ci_high': -0.02}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.