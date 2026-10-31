# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for ETH-USD. Long-only. Paper only.**

Data: ETH-USD 2024-10-18 00:00:00+00:00 to 2026-10-31 03:30:00+00:00 (744 days). Generated 2026-10-31 03:58:12.732528+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.03% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 224 | -0.681 | [-0.943, -0.389] | -0.038 | FAILED_OOS |
| donchian_breakout | 75 | -0.493 | [-0.937, 0.033] | -0.039 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 54 | -0.705 | [-1.218, -0.152] | -0.014 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 40 | -0.735 | [-1.171, -0.173] | -0.091 | INSUFFICIENT_SAMPLE |
| range_bounce | 84 | -0.68 | [-1.048, -0.31] | -0.015 | INSUFFICIENT_SAMPLE |
| btc_lead | 4 | -1.158 | [-2.213, 0.995] | -0.066 | INSUFFICIENT_SAMPLE |
| support_bounce | 62 | -0.749 | [-1.207, -0.239] | -0.042 | INSUFFICIENT_SAMPLE |
| swing_breakout | 91 | -0.512 | [-0.892, -0.075] | -0.039 | INSUFFICIENT_SAMPLE |
| steady_scalper | 244 | -0.375 | [-0.5, -0.234] | -0.028 | FAILED_OOS |
| zone_rejection | 6 | -0.57 | [-1.392, 1.305] | -0.113 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 73 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 73, 'mean_difference_R': 0.06, 'ci_low': -0.189, 'ci_high': 0.323, 'atr_exp_R': -0.523, 'chart_exp_R': -0.464}

Baseline (1h trend, one trade a day) OOS: {'trades': 67, 'win_rate': 0.343, 'avg_win_R': 1.181, 'avg_loss_R': -1.521, 'gross_expectancy_R': 0.083, 'net_expectancy_R': -0.594, 'cost_per_trade_R': 0.677, 'total_net_R': -39.76, 'profit_factor': 0.41, 'max_drawdown_R': 40.09, 'longest_losing_streak': 7, 't_stat': -3.47, 'ci_level': 0.9996, 'ci_low': -1.15, 'ci_high': -0.058}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.