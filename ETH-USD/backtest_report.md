# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for ETH-USD. Long-only. Paper only.**

Data: ETH-USD 2024-10-18 00:00:00+00:00 to 2026-11-07 03:45:00+00:00 (751 days). Generated 2026-11-07 04:04:58.528626+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.03% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 220 | -0.665 | [-0.946, -0.416] | -0.038 | FAILED_OOS |
| donchian_breakout | 75 | -0.451 | [-0.879, 0.088] | -0.027 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 51 | -0.634 | [-1.232, -0.012] | -0.004 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 42 | -0.7 | [-1.158, -0.181] | -0.085 | INSUFFICIENT_SAMPLE |
| range_bounce | 84 | -0.68 | [-1.048, -0.31] | -0.015 | INSUFFICIENT_SAMPLE |
| btc_lead | 4 | -1.158 | [-2.213, 0.995] | -0.066 | INSUFFICIENT_SAMPLE |
| support_bounce | 61 | -0.795 | [-1.225, -0.289] | -0.054 | INSUFFICIENT_SAMPLE |
| swing_breakout | 90 | -0.442 | [-0.845, -0.017] | -0.022 | INSUFFICIENT_SAMPLE |
| steady_scalper | 241 | -0.371 | [-0.493, -0.238] | -0.03 | FAILED_OOS |
| zone_rejection | 6 | -0.57 | [-1.392, 1.305] | -0.113 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 71 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 71, 'mean_difference_R': 0.033, 'ci_low': -0.214, 'ci_high': 0.278, 'atr_exp_R': -0.387, 'chart_exp_R': -0.354}

Baseline (1h trend, one trade a day) OOS: {'trades': 66, 'win_rate': 0.318, 'avg_win_R': 1.213, 'avg_loss_R': -1.556, 'gross_expectancy_R': -0.012, 'net_expectancy_R': -0.675, 'cost_per_trade_R': 0.663, 'total_net_R': -44.56, 'profit_factor': 0.36, 'max_drawdown_R': 44.79, 'longest_losing_streak': 7, 't_stat': -3.95, 'ci_level': 0.9996, 'ci_low': -1.188, 'ci_high': -0.094}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.