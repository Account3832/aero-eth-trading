# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for BNB-USD. Long-only. Paper only.**

Data: BNB-USD 2025-10-22 18:45:00+00:00 to 2026-11-14 10:15:00+00:00 (389 days). Generated 2026-11-14 10:34:14.407478+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 97 | -0.867 | [-1.313, -0.386] | -0.057 | INSUFFICIENT_SAMPLE |
| donchian_breakout | 40 | -0.733 | [-1.293, -0.094] | -0.078 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 18 | -0.958 | [-1.884, 0.063] | -0.032 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 15 | -0.857 | [-1.593, -0.029] | -0.06 | INSUFFICIENT_SAMPLE |
| range_bounce | 53 | -1.214 | [-1.663, -0.615] | -0.069 | INSUFFICIENT_SAMPLE |
| btc_lead | 10 | -0.93 | [-2.27, 0.334] | -0.023 | INSUFFICIENT_SAMPLE |
| support_bounce | 28 | -1.08 | [-1.866, 0.086] | -0.069 | INSUFFICIENT_SAMPLE |
| swing_breakout | 37 | -0.514 | [-1.123, 0.233] | -0.017 | INSUFFICIENT_SAMPLE |
| steady_scalper | 105 | -0.638 | [-0.875, -0.381] | -0.091 | FAILED_OOS |
| zone_rejection | 2 | 0.505 | [-0.453, 1.463] | 0.474 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 44 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 44, 'mean_difference_R': -0.05, 'ci_low': -0.301, 'ci_high': 0.168, 'atr_exp_R': -0.749, 'chart_exp_R': -0.799}

Baseline (1h trend, one trade a day) OOS: {'trades': 36, 'win_rate': 0.306, 'avg_win_R': 0.912, 'avg_loss_R': -1.669, 'gross_expectancy_R': -0.017, 'net_expectancy_R': -0.881, 'cost_per_trade_R': 0.864, 'total_net_R': -31.7, 'profit_factor': 0.24, 'max_drawdown_R': 29.37, 'longest_losing_streak': 9, 't_stat': -3.9, 'ci_level': 0.9996, 'ci_low': -1.506, 'ci_high': -0.121}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.