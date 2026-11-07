# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for ADA-USD. Long-only. Paper only.**

Data: ADA-USD 2024-10-20 00:00:00+00:00 to 2026-11-07 03:45:00+00:00 (749 days). Generated 2026-11-07 04:06:59.511238+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 167 | -0.344 | [-0.686, -0.021] | -0.051 | FAILED_OOS |
| donchian_breakout | 76 | -0.306 | [-0.75, 0.233] | -0.08 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 30 | -0.778 | [-1.267, -0.068] | -0.174 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 17 | -0.627 | [-1.267, 0.19] | -0.157 | INSUFFICIENT_SAMPLE |
| range_bounce | 87 | -0.589 | [-0.921, -0.261] | -0.067 | INSUFFICIENT_SAMPLE |
| btc_lead | 10 | -0.296 | [-1.349, 0.678] | 0.019 | INSUFFICIENT_SAMPLE |
| support_bounce | 39 | -0.586 | [-1.167, 0.105] | -0.098 | INSUFFICIENT_SAMPLE |
| swing_breakout | 96 | -0.485 | [-0.868, -0.034] | -0.165 | INSUFFICIENT_SAMPLE |
| steady_scalper | 190 | -0.219 | [-0.361, -0.079] | -0.061 | FAILED_OOS |
| zone_rejection | 2 | -1.327 | [-1.432, -1.222] | -0.407 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 76 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 76, 'mean_difference_R': 0.172, 'ci_low': -0.019, 'ci_high': 0.404, 'atr_exp_R': -0.267, 'chart_exp_R': -0.096}

Baseline (1h trend, one trade a day) OOS: {'trades': 59, 'win_rate': 0.424, 'avg_win_R': 1.166, 'avg_loss_R': -1.359, 'gross_expectancy_R': 0.116, 'net_expectancy_R': -0.289, 'cost_per_trade_R': 0.406, 'total_net_R': -17.07, 'profit_factor': 0.63, 'max_drawdown_R': 15.65, 'longest_losing_streak': 5, 't_stat': -1.65, 'ci_level': 0.9996, 'ci_low': -0.849, 'ci_high': 0.275}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.