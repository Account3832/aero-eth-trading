# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for AVAX-USD. Long-only. Paper only.**

Data: AVAX-USD 2024-10-20 00:00:00+00:00 to 2026-11-07 03:45:00+00:00 (749 days). Generated 2026-11-07 04:07:29.166634+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 10 | -0.6 | [-1.412, 0.625] | -0.103 | INSUFFICIENT_SAMPLE |
| donchian_breakout | 6 | -0.16 | [-1.336, 1.842] | 0.022 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 2 | 0.294 | [-1.426, 2.015] | 0.202 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 5 | -0.566 | [-1.396, 0.907] | -0.154 | INSUFFICIENT_SAMPLE |
| range_bounce | 6 | -0.21 | [-1.144, 0.801] | 0.037 | INSUFFICIENT_SAMPLE |
| btc_lead | 1 | -0.701 | n/a | -0.203 | INSUFFICIENT_SAMPLE |
| support_bounce | 3 | -1.415 | [-1.639, -1.223] | -0.326 | INSUFFICIENT_SAMPLE |
| swing_breakout | 7 | -0.714 | [-1.336, 1.155] | -0.224 | INSUFFICIENT_SAMPLE |
| steady_scalper | 13 | -0.336 | [-0.949, 0.245] | -0.094 | INSUFFICIENT_SAMPLE |
| zone_rejection | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 7 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 7, 'mean_difference_R': -0.69, 'ci_low': -1.101, 'ci_high': -0.239, 'atr_exp_R': 0.364, 'chart_exp_R': -0.327}

Baseline (1h trend, one trade a day) OOS: {'trades': 3, 'win_rate': 0.333, 'avg_win_R': 1.985, 'avg_loss_R': -1.442, 'gross_expectancy_R': 0.164, 'net_expectancy_R': -0.299, 'cost_per_trade_R': 0.464, 'total_net_R': -0.9, 'profit_factor': 0.69, 'max_drawdown_R': 1.37, 'longest_losing_streak': 2, 't_stat': -0.26, 'ci_level': 0.9996, 'ci_low': -1.51, 'ci_high': 1.985}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.