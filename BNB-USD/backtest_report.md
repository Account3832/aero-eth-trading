# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for BNB-USD. Long-only. Paper only.**

Data: BNB-USD 2025-10-22 18:45:00+00:00 to 2026-10-31 03:30:00+00:00 (375 days). Generated 2026-10-31 03:58:43.046067+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 106 | -0.848 | [-1.225, -0.444] | -0.048 | FAILED_OOS |
| donchian_breakout | 42 | -0.645 | [-1.218, 0.042] | -0.046 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 22 | -0.805 | [-1.639, 0.123] | -0.008 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 15 | -0.857 | [-1.593, -0.029] | -0.06 | INSUFFICIENT_SAMPLE |
| range_bounce | 45 | -1.133 | [-1.677, -0.468] | -0.047 | INSUFFICIENT_SAMPLE |
| btc_lead | 11 | -0.763 | [-2.216, 0.408] | -0.003 | INSUFFICIENT_SAMPLE |
| support_bounce | 28 | -1.038 | [-1.711, -0.009] | -0.059 | INSUFFICIENT_SAMPLE |
| swing_breakout | 39 | -0.529 | [-1.125, 0.171] | -0.017 | INSUFFICIENT_SAMPLE |
| steady_scalper | 119 | -0.645 | [-0.819, -0.45] | -0.083 | FAILED_OOS |
| zone_rejection | 2 | 0.505 | [-0.453, 1.463] | 0.474 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 49 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 49, 'mean_difference_R': -0.068, 'ci_low': -0.287, 'ci_high': 0.12, 'atr_exp_R': -0.734, 'chart_exp_R': -0.802}

Baseline (1h trend, one trade a day) OOS: {'trades': 40, 'win_rate': 0.3, 'avg_win_R': 0.962, 'avg_loss_R': -1.681, 'gross_expectancy_R': -0.017, 'net_expectancy_R': -0.888, 'cost_per_trade_R': 0.87, 'total_net_R': -35.51, 'profit_factor': 0.25, 'max_drawdown_R': 34.09, 'longest_losing_streak': 7, 't_stat': -4.11, 'ci_level': 0.9996, 'ci_low': -1.539, 'ci_high': -0.091}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.