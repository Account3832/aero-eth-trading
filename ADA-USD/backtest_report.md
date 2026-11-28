# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for ADA-USD. Long-only. Paper only.**

Data: ADA-USD 2024-10-20 00:00:00+00:00 to 2026-11-28 11:30:00+00:00 (770 days). Generated 2026-11-28 11:55:41.002216+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 167 | -0.421 | [-0.698, -0.083] | -0.086 | FAILED_OOS |
| donchian_breakout | 69 | -0.416 | [-0.87, 0.078] | -0.164 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 32 | -0.914 | [-1.323, -0.364] | -0.227 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 18 | -0.68 | [-1.281, 0.083] | -0.18 | INSUFFICIENT_SAMPLE |
| range_bounce | 98 | -0.55 | [-0.865, -0.196] | -0.059 | INSUFFICIENT_SAMPLE |
| btc_lead | 9 | -0.168 | [-1.153, 0.762] | 0.054 | INSUFFICIENT_SAMPLE |
| support_bounce | 45 | -0.565 | [-1.117, 0.037] | -0.09 | INSUFFICIENT_SAMPLE |
| swing_breakout | 96 | -0.583 | [-0.935, -0.177] | -0.233 | INSUFFICIENT_SAMPLE |
| steady_scalper | 190 | -0.239 | [-0.408, -0.093] | -0.077 | FAILED_OOS |
| zone_rejection | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 80 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 80, 'mean_difference_R': 0.182, 'ci_low': -0.013, 'ci_high': 0.385, 'atr_exp_R': -0.313, 'chart_exp_R': -0.131}

Baseline (1h trend, one trade a day) OOS: {'trades': 57, 'win_rate': 0.421, 'avg_win_R': 1.14, 'avg_loss_R': -1.348, 'gross_expectancy_R': 0.094, 'net_expectancy_R': -0.301, 'cost_per_trade_R': 0.395, 'total_net_R': -17.15, 'profit_factor': 0.61, 'max_drawdown_R': 19.71, 'longest_losing_streak': 9, 't_stat': -1.72, 'ci_level': 0.9996, 'ci_low': -0.793, 'ci_high': 0.266}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.