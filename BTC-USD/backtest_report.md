# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for BTC-USD. Long-only. Paper only.**

Data: BTC-USD 2024-10-18 00:00:00+00:00 to 2026-11-07 03:45:00+00:00 (751 days). Generated 2026-11-07 04:05:34.862519+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.02% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 213 | -0.855 | [-1.18, -0.529] | -0.034 | FAILED_OOS |
| donchian_breakout | 93 | -0.603 | [-1.004, -0.035] | -0.028 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 60 | -0.854 | [-1.442, -0.239] | -0.0 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 33 | -0.764 | [-1.325, -0.194] | -0.048 | INSUFFICIENT_SAMPLE |
| range_bounce | 70 | -1.059 | [-1.694, -0.548] | -0.015 | INSUFFICIENT_SAMPLE |
| btc_lead | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |
| support_bounce | 71 | -0.937 | [-1.481, -0.384] | -0.01 | INSUFFICIENT_SAMPLE |
| swing_breakout | 96 | -0.568 | [-0.951, -0.143] | -0.022 | INSUFFICIENT_SAMPLE |
| steady_scalper | 243 | -0.544 | [-0.687, -0.402] | -0.041 | FAILED_OOS |
| zone_rejection | 9 | -1.158 | [-2.019, 0.46] | -0.092 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 80 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 80, 'mean_difference_R': -0.022, 'ci_low': -0.21, 'ci_high': 0.159, 'atr_exp_R': -0.823, 'chart_exp_R': -0.845}

Baseline (1h trend, one trade a day) OOS: {'trades': 70, 'win_rate': 0.3, 'avg_win_R': 0.967, 'avg_loss_R': -1.695, 'gross_expectancy_R': -0.028, 'net_expectancy_R': -0.896, 'cost_per_trade_R': 0.868, 'total_net_R': -62.73, 'profit_factor': 0.24, 'max_drawdown_R': 62.76, 'longest_losing_streak': 8, 't_stat': -5.52, 'ci_level': 0.9996, 'ci_low': -1.346, 'ci_high': -0.341}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.