# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for AERO-USD. Long-only. Paper only.**

Data: AERO-USD 2024-10-18 00:00:00+00:00 to 2026-11-28 11:30:00+00:00 (772 days). Generated 2026-11-28 11:54:13.306869+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.1% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 203 | -0.263 | [-0.553, 0.123] | -0.035 | NOT_DEMONSTRATED |
| donchian_breakout | 81 | -0.292 | [-0.737, 0.257] | -0.114 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 40 | -0.578 | [-1.118, 0.065] | -0.126 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 21 | -0.365 | [-1.101, 0.367] | -0.068 | INSUFFICIENT_SAMPLE |
| range_bounce | 101 | -0.645 | [-0.976, -0.232] | -0.107 | FAILED_OOS |
| btc_lead | 7 | -0.514 | [-1.4, 1.088] | -0.193 | INSUFFICIENT_SAMPLE |
| support_bounce | 51 | -0.153 | [-0.791, 0.517] | 0.026 | INSUFFICIENT_SAMPLE |
| swing_breakout | 96 | -0.111 | [-0.531, 0.312] | 0.026 | INSUFFICIENT_SAMPLE |
| steady_scalper | 218 | -0.195 | [-0.345, -0.053] | -0.071 | FAILED_OOS |
| zone_rejection | 6 | -0.58 | [-1.311, 1.309] | -0.343 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 66 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 66, 'mean_difference_R': 0.048, 'ci_low': -0.194, 'ci_high': 0.293, 'atr_exp_R': -0.494, 'chart_exp_R': -0.447}

Baseline (1h trend, one trade a day) OOS: {'trades': 60, 'win_rate': 0.45, 'avg_win_R': 1.327, 'avg_loss_R': -1.282, 'gross_expectancy_R': 0.277, 'net_expectancy_R': -0.108, 'cost_per_trade_R': 0.385, 'total_net_R': -6.48, 'profit_factor': 0.85, 'max_drawdown_R': 16.51, 'longest_losing_streak': 6, 't_stat': -0.59, 'ci_level': 0.9996, 'ci_low': -0.617, 'ci_high': 0.561}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.