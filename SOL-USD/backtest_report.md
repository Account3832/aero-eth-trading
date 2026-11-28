# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for SOL-USD. Long-only. Paper only.**

Data: SOL-USD 2024-10-20 00:00:00+00:00 to 2026-11-28 11:30:00+00:00 (770 days). Generated 2026-11-28 11:55:07.072898+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 197 | -0.553 | [-0.8, -0.251] | -0.057 | FAILED_OOS |
| donchian_breakout | 77 | -0.259 | [-0.762, 0.236] | -0.003 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 56 | -0.596 | [-1.145, 0.05] | -0.042 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 38 | -0.714 | [-1.105, -0.228] | -0.138 | INSUFFICIENT_SAMPLE |
| range_bounce | 92 | -0.796 | [-1.148, -0.365] | -0.064 | INSUFFICIENT_SAMPLE |
| btc_lead | 7 | -0.899 | [-2.043, 0.176] | -0.103 | INSUFFICIENT_SAMPLE |
| support_bounce | 52 | -0.687 | [-1.225, -0.052] | -0.076 | INSUFFICIENT_SAMPLE |
| swing_breakout | 85 | -0.305 | [-0.706, 0.139] | -0.018 | INSUFFICIENT_SAMPLE |
| steady_scalper | 224 | -0.422 | [-0.585, -0.282] | -0.1 | FAILED_OOS |
| zone_rejection | 3 | -0.437 | [-1.253, 0.894] | -0.089 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 69 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 69, 'mean_difference_R': 0.125, 'ci_low': -0.097, 'ci_high': 0.352, 'atr_exp_R': -0.73, 'chart_exp_R': -0.605}

Baseline (1h trend, one trade a day) OOS: {'trades': 71, 'win_rate': 0.394, 'avg_win_R': 0.923, 'avg_loss_R': -1.508, 'gross_expectancy_R': 0.027, 'net_expectancy_R': -0.55, 'cost_per_trade_R': 0.577, 'total_net_R': -39.02, 'profit_factor': 0.4, 'max_drawdown_R': 38.22, 'longest_losing_streak': 7, 't_stat': -3.59, 'ci_level': 0.9996, 'ci_low': -1.021, 'ci_high': 0.001}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.