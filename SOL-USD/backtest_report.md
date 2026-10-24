# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for SOL-USD. Long-only. Paper only.**

Data: SOL-USD 2024-10-20 00:00:00+00:00 to 2026-10-24 03:30:00+00:00 (735 days). Generated 2026-10-24 03:50:31.793935+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 218 | -0.624 | [-0.869, -0.343] | -0.066 | FAILED_OOS |
| donchian_breakout | 90 | -0.344 | [-0.73, 0.046] | -0.029 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 57 | -0.643 | [-1.215, -0.108] | -0.042 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 36 | -0.656 | [-1.152, -0.124] | -0.107 | INSUFFICIENT_SAMPLE |
| range_bounce | 83 | -0.754 | [-1.191, -0.369] | -0.049 | INSUFFICIENT_SAMPLE |
| btc_lead | 8 | -0.981 | [-2.004, 0.097] | -0.121 | INSUFFICIENT_SAMPLE |
| support_bounce | 53 | -0.659 | [-1.149, -0.034] | -0.06 | INSUFFICIENT_SAMPLE |
| swing_breakout | 85 | -0.373 | [-0.866, 0.072] | -0.03 | INSUFFICIENT_SAMPLE |
| steady_scalper | 242 | -0.429 | [-0.599, -0.299] | -0.09 | FAILED_OOS |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 74 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 74, 'mean_difference_R': 0.099, 'ci_low': -0.117, 'ci_high': 0.319, 'atr_exp_R': -0.699, 'chart_exp_R': -0.6}

Baseline (1h trend, one trade a day) OOS: {'trades': 75, 'win_rate': 0.387, 'avg_win_R': 0.939, 'avg_loss_R': -1.527, 'gross_expectancy_R': 0.053, 'net_expectancy_R': -0.573, 'cost_per_trade_R': 0.627, 'total_net_R': -43.0, 'profit_factor': 0.39, 'max_drawdown_R': 41.72, 'longest_losing_streak': 8, 't_stat': -3.78, 'ci_level': 0.9995, 'ci_low': -1.089, 'ci_high': -0.034}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.