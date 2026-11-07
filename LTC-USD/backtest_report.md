# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for LTC-USD. Long-only. Paper only.**

Data: LTC-USD 2024-10-20 00:00:00+00:00 to 2026-11-07 03:45:00+00:00 (749 days). Generated 2026-11-07 04:07:42.037447+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 185 | -0.546 | [-0.853, -0.218] | -0.051 | FAILED_OOS |
| donchian_breakout | 60 | -0.413 | [-0.951, 0.309] | -0.053 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 30 | -0.606 | [-1.316, 0.168] | -0.03 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 15 | -0.201 | [-1.103, 0.697] | 0.043 | INSUFFICIENT_SAMPLE |
| range_bounce | 88 | -0.777 | [-1.139, -0.366] | -0.057 | INSUFFICIENT_SAMPLE |
| btc_lead | 14 | -0.688 | [-1.547, 0.374] | -0.046 | INSUFFICIENT_SAMPLE |
| support_bounce | 61 | -0.489 | [-1.039, 0.079] | -0.013 | INSUFFICIENT_SAMPLE |
| swing_breakout | 83 | -0.457 | [-0.825, -0.005] | -0.072 | INSUFFICIENT_SAMPLE |
| steady_scalper | 219 | -0.393 | [-0.534, -0.266] | -0.079 | FAILED_OOS |
| zone_rejection | 9 | -0.343 | [-1.489, 1.486] | 0.003 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 68 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 68, 'mean_difference_R': 0.104, 'ci_low': -0.178, 'ci_high': 0.379, 'atr_exp_R': -0.244, 'chart_exp_R': -0.14}

Baseline (1h trend, one trade a day) OOS: {'trades': 67, 'win_rate': 0.388, 'avg_win_R': 1.222, 'avg_loss_R': -1.518, 'gross_expectancy_R': 0.164, 'net_expectancy_R': -0.455, 'cost_per_trade_R': 0.619, 'total_net_R': -30.47, 'profit_factor': 0.51, 'max_drawdown_R': 30.55, 'longest_losing_streak': 5, 't_stat': -2.56, 'ci_level': 0.9996, 'ci_low': -0.929, 'ci_high': 0.14}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.