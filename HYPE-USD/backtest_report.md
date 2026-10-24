# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for HYPE-USD. Long-only. Paper only.**

Data: HYPE-USD 2026-02-05 19:30:00+00:00 to 2026-10-24 03:30:00+00:00 (262 days). Generated 2026-10-24 03:50:38.639293+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.08% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 73 | -0.604 | [-0.979, -0.17] | -0.135 | INSUFFICIENT_SAMPLE |
| donchian_breakout | 39 | -0.708 | [-1.309, -0.103] | -0.239 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 15 | -0.565 | [-1.526, 0.542] | -0.069 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 10 | -0.326 | [-1.347, 0.693] | -0.044 | INSUFFICIENT_SAMPLE |
| range_bounce | 20 | -0.932 | [-1.464, -0.13] | -0.179 | INSUFFICIENT_SAMPLE |
| btc_lead | 4 | -0.39 | [-1.254, 0.872] | -0.064 | INSUFFICIENT_SAMPLE |
| support_bounce | 24 | -0.218 | [-1.118, 0.87] | 0.025 | INSUFFICIENT_SAMPLE |
| swing_breakout | 33 | -0.599 | [-1.101, 0.006] | -0.176 | INSUFFICIENT_SAMPLE |
| steady_scalper | 81 | -0.335 | [-0.577, -0.109] | -0.108 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 26 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 26, 'mean_difference_R': 0.035, 'ci_low': -0.217, 'ci_high': 0.287, 'atr_exp_R': -0.491, 'chart_exp_R': -0.456}

Baseline (1h trend, one trade a day) OOS: {'trades': 29, 'win_rate': 0.241, 'avg_win_R': 1.504, 'avg_loss_R': -1.4, 'gross_expectancy_R': -0.203, 'net_expectancy_R': -0.699, 'cost_per_trade_R': 0.496, 'total_net_R': -20.28, 'profit_factor': 0.34, 'max_drawdown_R': 23.06, 'longest_losing_streak': 12, 't_stat': -2.89, 'ci_level': 0.9995, 'ci_low': -1.332, 'ci_high': 0.05}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.