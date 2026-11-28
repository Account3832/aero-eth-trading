# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for BNB-USD. Long-only. Paper only.**

Data: BNB-USD 2025-10-22 18:45:00+00:00 to 2026-11-28 11:30:00+00:00 (403 days). Generated 2026-11-28 11:54:40.926826+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 93 | -0.812 | [-1.226, -0.308] | -0.059 | INSUFFICIENT_SAMPLE |
| donchian_breakout | 40 | -0.741 | [-1.293, -0.089] | -0.096 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 15 | -0.464 | [-1.48, 0.903] | 0.03 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 15 | -0.371 | [-1.228, 0.481] | 0.017 | INSUFFICIENT_SAMPLE |
| range_bounce | 55 | -1.139 | [-1.528, -0.647] | -0.073 | INSUFFICIENT_SAMPLE |
| btc_lead | 5 | -0.32 | [-1.753, 0.77] | 0.035 | INSUFFICIENT_SAMPLE |
| support_bounce | 28 | -0.889 | [-1.635, 0.211] | -0.056 | INSUFFICIENT_SAMPLE |
| swing_breakout | 37 | -0.589 | [-1.211, 0.058] | -0.05 | INSUFFICIENT_SAMPLE |
| steady_scalper | 100 | -0.574 | [-0.841, -0.298] | -0.088 | FAILED_OOS |
| zone_rejection | 2 | 0.505 | [-0.453, 1.463] | 0.474 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 42 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 42, 'mean_difference_R': -0.042, 'ci_low': -0.306, 'ci_high': 0.187, 'atr_exp_R': -0.738, 'chart_exp_R': -0.779}

Baseline (1h trend, one trade a day) OOS: {'trades': 34, 'win_rate': 0.294, 'avg_win_R': 0.848, 'avg_loss_R': -1.584, 'gross_expectancy_R': -0.075, 'net_expectancy_R': -0.869, 'cost_per_trade_R': 0.794, 'total_net_R': -29.54, 'profit_factor': 0.22, 'max_drawdown_R': 28.68, 'longest_losing_streak': 12, 't_stat': -3.99, 'ci_level': 0.9996, 'ci_low': -1.547, 'ci_high': -0.127}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.