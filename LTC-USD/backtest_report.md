# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for LTC-USD. Long-only. Paper only.**

Data: LTC-USD 2024-10-20 00:00:00+00:00 to 2026-10-24 03:30:00+00:00 (735 days). Generated 2026-10-24 03:51:08.354849+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 186 | -0.574 | [-0.878, -0.235] | -0.055 | FAILED_OOS |
| donchian_breakout | 62 | -0.425 | [-0.982, 0.176] | -0.054 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 34 | -0.737 | [-1.424, 0.002] | -0.053 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 15 | -0.099 | [-1.153, 0.799] | 0.072 | INSUFFICIENT_SAMPLE |
| range_bounce | 91 | -0.812 | [-1.168, -0.473] | -0.059 | INSUFFICIENT_SAMPLE |
| btc_lead | 14 | -0.52 | [-1.45, 0.371] | -0.006 | INSUFFICIENT_SAMPLE |
| support_bounce | 60 | -0.48 | [-1.009, 0.073] | -0.009 | INSUFFICIENT_SAMPLE |
| swing_breakout | 80 | -0.469 | [-0.884, 0.008] | -0.073 | INSUFFICIENT_SAMPLE |
| steady_scalper | 217 | -0.39 | [-0.526, -0.243] | -0.074 | FAILED_OOS |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 69 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 69, 'mean_difference_R': 0.11, 'ci_low': -0.15, 'ci_high': 0.382, 'atr_exp_R': -0.288, 'chart_exp_R': -0.178}

Baseline (1h trend, one trade a day) OOS: {'trades': 68, 'win_rate': 0.382, 'avg_win_R': 1.222, 'avg_loss_R': -1.531, 'gross_expectancy_R': 0.15, 'net_expectancy_R': -0.478, 'cost_per_trade_R': 0.628, 'total_net_R': -32.52, 'profit_factor': 0.49, 'max_drawdown_R': 30.87, 'longest_losing_streak': 5, 't_stat': -2.7, 'ci_level': 0.9995, 'ci_low': -1.035, 'ci_high': 0.13}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.