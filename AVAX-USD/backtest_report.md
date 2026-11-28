# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for AVAX-USD. Long-only. Paper only.**

Data: AVAX-USD 2024-10-20 00:00:00+00:00 to 2026-11-28 11:30:00+00:00 (770 days). Generated 2026-11-28 11:56:06.172611+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 20 | -0.592 | [-1.295, 0.318] | -0.116 | INSUFFICIENT_SAMPLE |
| donchian_breakout | 10 | -0.385 | [-1.279, 1.204] | -0.118 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 5 | -0.365 | [-1.472, 1.716] | -0.019 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 12 | -0.278 | [-1.155, 0.714] | -0.023 | INSUFFICIENT_SAMPLE |
| range_bounce | 20 | -0.516 | [-1.147, 0.301] | -0.043 | INSUFFICIENT_SAMPLE |
| btc_lead | 1 | -0.701 | n/a | -0.203 | INSUFFICIENT_SAMPLE |
| support_bounce | 8 | -0.907 | [-1.504, 0.754] | -0.2 | INSUFFICIENT_SAMPLE |
| swing_breakout | 13 | -0.63 | [-1.252, 0.52] | -0.21 | INSUFFICIENT_SAMPLE |
| steady_scalper | 26 | -0.344 | [-0.727, 0.133] | -0.103 | INSUFFICIENT_SAMPLE |
| zone_rejection | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 13 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 13, 'mean_difference_R': -0.609, 'ci_low': -1.02, 'ci_high': -0.198, 'atr_exp_R': -0.132, 'chart_exp_R': -0.741}

Baseline (1h trend, one trade a day) OOS: {'trades': 9, 'win_rate': 0.333, 'avg_win_R': 0.872, 'avg_loss_R': -1.446, 'gross_expectancy_R': -0.201, 'net_expectancy_R': -0.673, 'cost_per_trade_R': 0.472, 'total_net_R': -6.06, 'profit_factor': 0.3, 'max_drawdown_R': 5.16, 'longest_losing_streak': 3, 't_stat': -1.6, 'ci_level': 0.9996, 'ci_low': -1.496, 'ci_high': 0.797}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.