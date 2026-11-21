# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for BNB-USD. Long-only. Paper only.**

Data: BNB-USD 2025-10-22 18:45:00+00:00 to 2026-11-21 10:45:00+00:00 (396 days). Generated 2026-11-21 11:13:59.171271+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 92 | -0.843 | [-1.299, -0.372] | -0.057 | INSUFFICIENT_SAMPLE |
| donchian_breakout | 40 | -0.729 | [-1.307, -0.106] | -0.079 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 14 | -0.622 | [-1.629, 0.701] | 0.008 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 11 | -0.619 | [-1.507, 0.359] | -0.024 | INSUFFICIENT_SAMPLE |
| range_bounce | 55 | -1.213 | [-1.643, -0.777] | -0.074 | INSUFFICIENT_SAMPLE |
| btc_lead | 10 | -0.93 | [-2.27, 0.334] | -0.023 | INSUFFICIENT_SAMPLE |
| support_bounce | 26 | -0.978 | [-1.693, -0.06] | -0.062 | INSUFFICIENT_SAMPLE |
| swing_breakout | 37 | -0.51 | [-1.197, 0.277] | -0.017 | INSUFFICIENT_SAMPLE |
| steady_scalper | 100 | -0.627 | [-0.866, -0.389] | -0.092 | FAILED_OOS |
| zone_rejection | 2 | 0.505 | [-0.453, 1.463] | 0.474 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 43 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 43, 'mean_difference_R': -0.06, 'ci_low': -0.311, 'ci_high': 0.162, 'atr_exp_R': -0.724, 'chart_exp_R': -0.784}

Baseline (1h trend, one trade a day) OOS: {'trades': 33, 'win_rate': 0.303, 'avg_win_R': 0.848, 'avg_loss_R': -1.612, 'gross_expectancy_R': -0.047, 'net_expectancy_R': -0.867, 'cost_per_trade_R': 0.82, 'total_net_R': -28.6, 'profit_factor': 0.23, 'max_drawdown_R': 26.24, 'longest_losing_streak': 10, 't_stat': -3.83, 'ci_level': 0.9996, 'ci_low': -1.526, 'ci_high': -0.081}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.