# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for ADA-USD. Long-only. Paper only.**

Data: ADA-USD 2024-10-20 00:00:00+00:00 to 2026-11-14 10:15:00+00:00 (756 days). Generated 2026-11-14 10:35:28.079849+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 160 | -0.379 | [-0.686, -0.022] | -0.07 | FAILED_OOS |
| donchian_breakout | 72 | -0.389 | [-0.884, 0.096] | -0.137 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 30 | -0.778 | [-1.267, -0.068] | -0.174 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 17 | -0.627 | [-1.267, 0.19] | -0.157 | INSUFFICIENT_SAMPLE |
| range_bounce | 90 | -0.611 | [-0.935, -0.241] | -0.074 | INSUFFICIENT_SAMPLE |
| btc_lead | 9 | -0.168 | [-1.153, 0.762] | 0.054 | INSUFFICIENT_SAMPLE |
| support_bounce | 39 | -0.586 | [-1.167, 0.105] | -0.098 | INSUFFICIENT_SAMPLE |
| swing_breakout | 92 | -0.565 | [-0.96, -0.126] | -0.215 | INSUFFICIENT_SAMPLE |
| steady_scalper | 181 | -0.22 | [-0.372, -0.067] | -0.066 | FAILED_OOS |
| zone_rejection | 2 | -1.327 | [-1.432, -1.222] | -0.407 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 73 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 73, 'mean_difference_R': 0.149, 'ci_low': -0.048, 'ci_high': 0.39, 'atr_exp_R': -0.278, 'chart_exp_R': -0.128}

Baseline (1h trend, one trade a day) OOS: {'trades': 54, 'win_rate': 0.463, 'avg_win_R': 1.166, 'avg_loss_R': -1.336, 'gross_expectancy_R': 0.21, 'net_expectancy_R': -0.177, 'cost_per_trade_R': 0.388, 'total_net_R': -9.58, 'profit_factor': 0.75, 'max_drawdown_R': 12.56, 'longest_losing_streak': 5, 't_stat': -0.97, 'ci_level': 0.9996, 'ci_low': -0.707, 'ci_high': 0.476}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.