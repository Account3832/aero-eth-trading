# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for LTC-USD. Long-only. Paper only.**

Data: LTC-USD 2024-10-20 00:00:00+00:00 to 2026-10-31 03:30:00+00:00 (742 days). Generated 2026-10-31 03:59:51.790785+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 189 | -0.554 | [-0.806, -0.293] | -0.051 | FAILED_OOS |
| donchian_breakout | 61 | -0.408 | [-0.942, 0.086] | -0.049 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 32 | -0.676 | [-1.34, 0.268] | -0.042 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 16 | -0.165 | [-1.073, 0.599] | 0.052 | INSUFFICIENT_SAMPLE |
| range_bounce | 87 | -0.76 | [-1.115, -0.389] | -0.052 | INSUFFICIENT_SAMPLE |
| btc_lead | 13 | -0.618 | [-1.571, 0.352] | -0.031 | INSUFFICIENT_SAMPLE |
| support_bounce | 62 | -0.486 | [-1.029, 0.121] | -0.01 | INSUFFICIENT_SAMPLE |
| swing_breakout | 81 | -0.476 | [-0.87, -0.049] | -0.078 | INSUFFICIENT_SAMPLE |
| steady_scalper | 222 | -0.39 | [-0.552, -0.232] | -0.076 | FAILED_OOS |
| zone_rejection | 9 | -0.343 | [-1.489, 1.486] | 0.003 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 69 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 69, 'mean_difference_R': 0.103, 'ci_low': -0.16, 'ci_high': 0.376, 'atr_exp_R': -0.261, 'chart_exp_R': -0.158}

Baseline (1h trend, one trade a day) OOS: {'trades': 67, 'win_rate': 0.388, 'avg_win_R': 1.222, 'avg_loss_R': -1.517, 'gross_expectancy_R': 0.164, 'net_expectancy_R': -0.454, 'cost_per_trade_R': 0.618, 'total_net_R': -30.41, 'profit_factor': 0.51, 'max_drawdown_R': 29.02, 'longest_losing_streak': 5, 't_stat': -2.55, 'ci_level': 0.9996, 'ci_low': -1.124, 'ci_high': 0.208}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.