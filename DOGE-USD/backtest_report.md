# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for DOGE-USD. Long-only. Paper only.**

Data: DOGE-USD 2024-10-20 00:00:00+00:00 to 2026-11-21 10:45:00+00:00 (763 days). Generated 2026-11-21 11:14:52.572720+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 153 | -0.546 | [-0.877, -0.18] | -0.066 | FAILED_OOS |
| donchian_breakout | 64 | -0.382 | [-0.874, 0.28] | -0.047 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 34 | -0.548 | [-1.321, 0.524] | -0.025 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 28 | -0.302 | [-0.948, 0.262] | 0.003 | INSUFFICIENT_SAMPLE |
| range_bounce | 87 | -0.864 | [-1.244, -0.489] | -0.08 | INSUFFICIENT_SAMPLE |
| btc_lead | 6 | -0.59 | [-1.775, 0.767] | -0.019 | INSUFFICIENT_SAMPLE |
| support_bounce | 68 | -0.813 | [-1.187, -0.313] | -0.101 | INSUFFICIENT_SAMPLE |
| swing_breakout | 75 | -0.502 | [-0.984, 0.044] | -0.073 | INSUFFICIENT_SAMPLE |
| steady_scalper | 170 | -0.368 | [-0.528, -0.192] | -0.084 | FAILED_OOS |
| zone_rejection | 2 | 2.608 | [2.154, 3.063] | 1.161 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 45 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 45, 'mean_difference_R': 0.093, 'ci_low': -0.202, 'ci_high': 0.422, 'atr_exp_R': -0.52, 'chart_exp_R': -0.427}

Baseline (1h trend, one trade a day) OOS: {'trades': 53, 'win_rate': 0.509, 'avg_win_R': 0.98, 'avg_loss_R': -1.501, 'gross_expectancy_R': 0.36, 'net_expectancy_R': -0.237, 'cost_per_trade_R': 0.598, 'total_net_R': -12.58, 'profit_factor': 0.68, 'max_drawdown_R': 14.86, 'longest_losing_streak': 5, 't_stat': -1.28, 'ci_level': 0.9996, 'ci_low': -0.758, 'ci_high': 0.414}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.