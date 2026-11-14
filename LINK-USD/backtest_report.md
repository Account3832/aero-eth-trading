# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for LINK-USD. Long-only. Paper only.**

Data: LINK-USD 2024-10-20 00:00:00+00:00 to 2026-11-14 10:15:00+00:00 (756 days). Generated 2026-11-14 10:35:45.974760+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 199 | -0.533 | [-0.815, -0.238] | -0.063 | FAILED_OOS |
| donchian_breakout | 78 | -0.179 | [-0.726, 0.432] | 0.024 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 49 | -0.87 | [-1.333, -0.312] | -0.106 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 29 | -0.535 | [-1.113, 0.127] | -0.082 | INSUFFICIENT_SAMPLE |
| range_bounce | 88 | -0.654 | [-0.977, -0.285] | -0.053 | INSUFFICIENT_SAMPLE |
| btc_lead | 3 | 0.001 | [-1.332, 1.075] | 0.1 | INSUFFICIENT_SAMPLE |
| support_bounce | 51 | -0.468 | [-1.076, 0.284] | -0.032 | INSUFFICIENT_SAMPLE |
| swing_breakout | 95 | -0.265 | [-0.72, 0.2] | -0.005 | INSUFFICIENT_SAMPLE |
| steady_scalper | 230 | -0.406 | [-0.543, -0.257] | -0.108 | FAILED_OOS |
| zone_rejection | 7 | 0.111 | [-1.395, 2.022] | 0.145 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 64 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 64, 'mean_difference_R': 0.023, 'ci_low': -0.198, 'ci_high': 0.263, 'atr_exp_R': -0.256, 'chart_exp_R': -0.232}

Baseline (1h trend, one trade a day) OOS: {'trades': 68, 'win_rate': 0.353, 'avg_win_R': 1.039, 'avg_loss_R': -1.411, 'gross_expectancy_R': -0.019, 'net_expectancy_R': -0.546, 'cost_per_trade_R': 0.528, 'total_net_R': -37.14, 'profit_factor': 0.4, 'max_drawdown_R': 39.5, 'longest_losing_streak': 8, 't_stat': -3.52, 'ci_level': 0.9996, 'ci_low': -1.066, 'ci_high': 0.029}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.