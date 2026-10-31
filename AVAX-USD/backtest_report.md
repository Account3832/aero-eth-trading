# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for AVAX-USD. Long-only. Paper only.**

Data: AVAX-USD 2024-10-20 00:00:00+00:00 to 2026-10-31 03:30:00+00:00 (742 days). Generated 2026-10-31 03:59:43.972610+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 5 | -0.679 | [-1.488, 0.453] | -0.118 | INSUFFICIENT_SAMPLE |
| donchian_breakout | 3 | -1.265 | [-1.368, -1.188] | -0.507 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |
| oversold_bounce | 2 | -0.649 | [-1.245, -0.053] | -0.492 | INSUFFICIENT_SAMPLE |
| range_bounce | 2 | -0.528 | [-1.387, 0.33] | -0.13 | INSUFFICIENT_SAMPLE |
| btc_lead | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |
| support_bounce | 1 | -1.382 | n/a | -0.353 | INSUFFICIENT_SAMPLE |
| swing_breakout | 5 | -1.251 | [-1.366, -1.125] | -0.489 | INSUFFICIENT_SAMPLE |
| steady_scalper | 6 | -0.45 | [-1.163, 0.225] | -0.138 | INSUFFICIENT_SAMPLE |
| zone_rejection | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 3 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 3, 'mean_difference_R': -0.423, 'ci_low': -1.375, 'ci_high': 0.071, 'atr_exp_R': -0.765, 'chart_exp_R': -1.189}

Baseline (1h trend, one trade a day) OOS: {'trades': 1, 'win_rate': 0.0, 'avg_win_R': 0.0, 'avg_loss_R': -1.51, 'gross_expectancy_R': -0.898, 'net_expectancy_R': -1.51, 'cost_per_trade_R': 0.612, 'total_net_R': -1.51, 'profit_factor': 0.0, 'max_drawdown_R': 0.0, 'longest_losing_streak': 1, 't_stat': None, 'ci_level': 0.9996, 'ci_low': nan, 'ci_high': nan}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.