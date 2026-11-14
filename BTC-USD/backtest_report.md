# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for BTC-USD. Long-only. Paper only.**

Data: BTC-USD 2024-10-18 00:00:00+00:00 to 2026-11-14 10:15:00+00:00 (758 days). Generated 2026-11-14 10:34:00.562661+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.02% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 204 | -0.865 | [-1.163, -0.608] | -0.034 | FAILED_OOS |
| donchian_breakout | 91 | -0.614 | [-1.053, -0.125] | -0.027 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 60 | -0.854 | [-1.442, -0.239] | -0.0 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 32 | -0.812 | [-1.309, -0.247] | -0.056 | INSUFFICIENT_SAMPLE |
| range_bounce | 72 | -1.041 | [-1.585, -0.545] | -0.013 | INSUFFICIENT_SAMPLE |
| btc_lead | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |
| support_bounce | 69 | -0.949 | [-1.598, -0.347] | -0.008 | INSUFFICIENT_SAMPLE |
| swing_breakout | 96 | -0.625 | [-1.019, -0.248] | -0.033 | INSUFFICIENT_SAMPLE |
| steady_scalper | 234 | -0.559 | [-0.729, -0.417] | -0.043 | FAILED_OOS |
| zone_rejection | 7 | -1.484 | [-2.166, 0.158] | -0.111 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 72 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 72, 'mean_difference_R': -0.081, 'ci_low': -0.285, 'ci_high': 0.12, 'atr_exp_R': -0.826, 'chart_exp_R': -0.907}

Baseline (1h trend, one trade a day) OOS: {'trades': 68, 'win_rate': 0.294, 'avg_win_R': 1.014, 'avg_loss_R': -1.698, 'gross_expectancy_R': -0.027, 'net_expectancy_R': -0.9, 'cost_per_trade_R': 0.873, 'total_net_R': -61.21, 'profit_factor': 0.25, 'max_drawdown_R': 62.25, 'longest_losing_streak': 8, 't_stat': -5.41, 'ci_level': 0.9996, 'ci_low': -1.428, 'ci_high': -0.39}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.