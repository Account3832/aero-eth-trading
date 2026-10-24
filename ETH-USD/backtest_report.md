# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for ETH-USD. Long-only. Paper only.**

Data: ETH-USD 2024-10-18 00:00:00+00:00 to 2026-10-24 03:30:00+00:00 (737 days). Generated 2026-10-24 03:49:56.779595+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.03% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 225 | -0.692 | [-0.988, -0.418] | -0.039 | FAILED_OOS |
| donchian_breakout | 75 | -0.494 | [-0.915, -0.014] | -0.039 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 53 | -0.766 | [-1.342, -0.092] | -0.022 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 39 | -0.762 | [-1.246, -0.291] | -0.095 | INSUFFICIENT_SAMPLE |
| range_bounce | 84 | -0.71 | [-1.09, -0.277] | -0.018 | INSUFFICIENT_SAMPLE |
| btc_lead | 4 | -1.158 | [-2.213, 0.995] | -0.066 | INSUFFICIENT_SAMPLE |
| support_bounce | 62 | -0.702 | [-1.192, -0.146] | -0.032 | INSUFFICIENT_SAMPLE |
| swing_breakout | 91 | -0.514 | [-0.941, -0.057] | -0.039 | INSUFFICIENT_SAMPLE |
| steady_scalper | 244 | -0.37 | [-0.518, -0.238] | -0.026 | FAILED_OOS |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 73 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 73, 'mean_difference_R': 0.093, 'ci_low': -0.174, 'ci_high': 0.356, 'atr_exp_R': -0.483, 'chart_exp_R': -0.39}

Baseline (1h trend, one trade a day) OOS: {'trades': 67, 'win_rate': 0.343, 'avg_win_R': 1.181, 'avg_loss_R': -1.53, 'gross_expectancy_R': 0.084, 'net_expectancy_R': -0.6, 'cost_per_trade_R': 0.684, 'total_net_R': -40.17, 'profit_factor': 0.4, 'max_drawdown_R': 38.74, 'longest_losing_streak': 7, 't_stat': -3.49, 'ci_level': 0.9995, 'ci_low': -1.131, 'ci_high': 0.006}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.