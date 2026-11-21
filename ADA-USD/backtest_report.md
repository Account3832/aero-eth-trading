# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for ADA-USD. Long-only. Paper only.**

Data: ADA-USD 2024-10-20 00:00:00+00:00 to 2026-11-21 10:45:00+00:00 (763 days). Generated 2026-11-21 11:15:09.859884+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 159 | -0.417 | [-0.733, -0.115] | -0.086 | FAILED_OOS |
| donchian_breakout | 69 | -0.446 | [-0.867, 0.024] | -0.177 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 30 | -0.884 | [-1.305, -0.272] | -0.216 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 17 | -0.627 | [-1.267, 0.19] | -0.157 | INSUFFICIENT_SAMPLE |
| range_bounce | 92 | -0.567 | [-0.863, -0.261] | -0.063 | INSUFFICIENT_SAMPLE |
| btc_lead | 9 | -0.168 | [-1.153, 0.762] | 0.054 | INSUFFICIENT_SAMPLE |
| support_bounce | 41 | -0.538 | [-1.112, 0.228] | -0.083 | INSUFFICIENT_SAMPLE |
| swing_breakout | 93 | -0.605 | [-0.96, -0.119] | -0.242 | INSUFFICIENT_SAMPLE |
| steady_scalper | 179 | -0.23 | [-0.384, -0.086] | -0.073 | FAILED_OOS |
| zone_rejection | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 75 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 75, 'mean_difference_R': 0.148, 'ci_low': -0.048, 'ci_high': 0.378, 'atr_exp_R': -0.307, 'chart_exp_R': -0.159}

Baseline (1h trend, one trade a day) OOS: {'trades': 53, 'win_rate': 0.453, 'avg_win_R': 1.14, 'avg_loss_R': -1.339, 'gross_expectancy_R': 0.17, 'net_expectancy_R': -0.216, 'cost_per_trade_R': 0.387, 'total_net_R': -11.47, 'profit_factor': 0.7, 'max_drawdown_R': 14.03, 'longest_losing_streak': 5, 't_stat': -1.18, 'ci_level': 0.9996, 'ci_low': -0.804, 'ci_high': 0.438}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.