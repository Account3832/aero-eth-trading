# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for BTC-USD. Long-only. Paper only.**

Data: BTC-USD 2024-10-18 00:00:00+00:00 to 2026-10-31 03:30:00+00:00 (744 days). Generated 2026-10-31 03:58:35.006991+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.02% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 219 | -0.869 | [-1.186, -0.605] | -0.034 | FAILED_OOS |
| donchian_breakout | 93 | -0.601 | [-1.036, -0.142] | -0.028 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 64 | -0.834 | [-1.349, -0.28] | 0.003 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 32 | -0.75 | [-1.299, -0.201] | -0.043 | INSUFFICIENT_SAMPLE |
| range_bounce | 67 | -1.066 | [-1.562, -0.57] | -0.015 | INSUFFICIENT_SAMPLE |
| btc_lead | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |
| support_bounce | 73 | -0.883 | [-1.498, -0.398] | -0.004 | INSUFFICIENT_SAMPLE |
| swing_breakout | 95 | -0.555 | [-0.944, -0.165] | -0.019 | INSUFFICIENT_SAMPLE |
| steady_scalper | 247 | -0.555 | [-0.685, -0.416] | -0.041 | FAILED_OOS |
| zone_rejection | 9 | -1.158 | [-2.019, 0.46] | -0.092 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 82 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 82, 'mean_difference_R': -0.023, 'ci_low': -0.215, 'ci_high': 0.163, 'atr_exp_R': -0.825, 'chart_exp_R': -0.847}

Baseline (1h trend, one trade a day) OOS: {'trades': 72, 'win_rate': 0.319, 'avg_win_R': 0.99, 'avg_loss_R': -1.675, 'gross_expectancy_R': 0.056, 'net_expectancy_R': -0.824, 'cost_per_trade_R': 0.88, 'total_net_R': -59.3, 'profit_factor': 0.28, 'max_drawdown_R': 60.11, 'longest_losing_streak': 8, 't_stat': -5.06, 'ci_level': 0.9996, 'ci_low': -1.343, 'ci_high': -0.273}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.