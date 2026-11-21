# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for XRP-USD. Long-only. Paper only.**

Data: XRP-USD 2024-10-20 00:00:00+00:00 to 2026-11-21 10:45:00+00:00 (763 days). Generated 2026-11-21 11:14:11.949824+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 173 | -0.567 | [-0.889, -0.25] | -0.069 | FAILED_OOS |
| donchian_breakout | 82 | -0.331 | [-0.798, 0.23] | -0.033 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 37 | -0.462 | [-1.323, 0.443] | -0.003 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 22 | -0.414 | [-1.023, 0.353] | -0.029 | INSUFFICIENT_SAMPLE |
| range_bounce | 99 | -0.813 | [-1.155, -0.48] | -0.051 | INSUFFICIENT_SAMPLE |
| btc_lead | 5 | -0.834 | [-2.533, 0.485] | -0.011 | INSUFFICIENT_SAMPLE |
| support_bounce | 45 | -0.349 | [-1.089, 0.382] | 0.019 | INSUFFICIENT_SAMPLE |
| swing_breakout | 88 | -0.377 | [-0.833, 0.068] | -0.035 | INSUFFICIENT_SAMPLE |
| steady_scalper | 195 | -0.36 | [-0.487, -0.201] | -0.079 | FAILED_OOS |
| zone_rejection | 6 | -1.275 | [-1.401, -1.135] | -0.48 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 56 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 56, 'mean_difference_R': 0.073, 'ci_low': -0.123, 'ci_high': 0.282, 'atr_exp_R': -0.536, 'chart_exp_R': -0.463}

Baseline (1h trend, one trade a day) OOS: {'trades': 54, 'win_rate': 0.481, 'avg_win_R': 1.148, 'avg_loss_R': -1.383, 'gross_expectancy_R': 0.395, 'net_expectancy_R': -0.165, 'cost_per_trade_R': 0.559, 'total_net_R': -8.89, 'profit_factor': 0.77, 'max_drawdown_R': 10.95, 'longest_losing_streak': 5, 't_stat': -0.87, 'ci_level': 0.9996, 'ci_low': -0.765, 'ci_high': 0.523}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.