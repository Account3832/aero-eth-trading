# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for LTC-USD. Long-only. Paper only.**

Data: LTC-USD 2024-10-20 00:00:00+00:00 to 2026-11-28 11:30:00+00:00 (770 days). Generated 2026-11-28 11:56:17.216279+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 174 | -0.568 | [-0.899, -0.252] | -0.06 | FAILED_OOS |
| donchian_breakout | 58 | -0.539 | [-1.04, -0.036] | -0.103 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 32 | -0.639 | [-1.256, 0.127] | -0.043 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 10 | -0.493 | [-1.441, 0.823] | -0.046 | INSUFFICIENT_SAMPLE |
| range_bounce | 99 | -0.699 | [-1.026, -0.29] | -0.043 | INSUFFICIENT_SAMPLE |
| btc_lead | 13 | -0.581 | [-1.42, 0.478] | -0.032 | INSUFFICIENT_SAMPLE |
| support_bounce | 61 | -0.57 | [-1.043, 0.003] | -0.033 | INSUFFICIENT_SAMPLE |
| swing_breakout | 81 | -0.524 | [-0.989, -0.059] | -0.103 | INSUFFICIENT_SAMPLE |
| steady_scalper | 202 | -0.399 | [-0.592, -0.232] | -0.085 | FAILED_OOS |
| zone_rejection | 6 | -0.587 | [-1.637, 1.251] | -0.076 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 67 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 67, 'mean_difference_R': 0.082, 'ci_low': -0.203, 'ci_high': 0.361, 'atr_exp_R': -0.346, 'chart_exp_R': -0.264}

Baseline (1h trend, one trade a day) OOS: {'trades': 64, 'win_rate': 0.375, 'avg_win_R': 1.249, 'avg_loss_R': -1.506, 'gross_expectancy_R': 0.133, 'net_expectancy_R': -0.473, 'cost_per_trade_R': 0.606, 'total_net_R': -30.25, 'profit_factor': 0.5, 'max_drawdown_R': 28.4, 'longest_losing_streak': 7, 't_stat': -2.61, 'ci_level': 0.9996, 'ci_low': -1.047, 'ci_high': 0.108}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.