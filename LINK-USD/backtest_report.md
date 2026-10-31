# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for LINK-USD. Long-only. Paper only.**

Data: LINK-USD 2024-10-20 00:00:00+00:00 to 2026-10-31 03:30:00+00:00 (742 days). Generated 2026-10-31 03:59:36.555978+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 215 | -0.537 | [-0.795, -0.229] | -0.059 | FAILED_OOS |
| donchian_breakout | 82 | -0.138 | [-0.643, 0.361] | 0.042 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 51 | -0.913 | [-1.379, -0.353] | -0.11 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 29 | -0.502 | [-1.123, 0.141] | -0.069 | INSUFFICIENT_SAMPLE |
| range_bounce | 79 | -0.695 | [-1.029, -0.234] | -0.059 | INSUFFICIENT_SAMPLE |
| btc_lead | 3 | 0.001 | [-1.332, 1.075] | 0.1 | INSUFFICIENT_SAMPLE |
| support_bounce | 51 | -0.545 | [-1.081, 0.174] | -0.049 | INSUFFICIENT_SAMPLE |
| swing_breakout | 100 | -0.18 | [-0.62, 0.295] | 0.03 | NOT_DEMONSTRATED |
| steady_scalper | 247 | -0.399 | [-0.532, -0.243] | -0.099 | FAILED_OOS |
| zone_rejection | 8 | 0.312 | [-1.343, 1.968] | 0.227 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 72 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 72, 'mean_difference_R': 0.1, 'ci_low': -0.118, 'ci_high': 0.333, 'atr_exp_R': -0.263, 'chart_exp_R': -0.164}

Baseline (1h trend, one trade a day) OOS: {'trades': 73, 'win_rate': 0.329, 'avg_win_R': 1.033, 'avg_loss_R': -1.429, 'gross_expectancy_R': -0.082, 'net_expectancy_R': -0.62, 'cost_per_trade_R': 0.537, 'total_net_R': -45.24, 'profit_factor': 0.35, 'max_drawdown_R': 43.64, 'longest_losing_streak': 8, 't_stat': -4.2, 'ci_level': 0.9996, 'ci_low': -1.059, 'ci_high': -0.114}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.