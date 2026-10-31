# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for AERO-USD. Long-only. Paper only.**

Data: AERO-USD 2024-10-18 00:00:00+00:00 to 2026-10-31 03:30:00+00:00 (744 days). Generated 2026-10-31 03:58:23.270364+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.1% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 208 | -0.224 | [-0.609, 0.067] | -0.016 | NOT_DEMONSTRATED |
| donchian_breakout | 86 | -0.324 | [-0.736, 0.088] | -0.134 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 38 | -0.541 | [-1.088, 0.257] | -0.108 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 24 | -0.539 | [-1.198, 0.184] | -0.152 | INSUFFICIENT_SAMPLE |
| range_bounce | 91 | -0.638 | [-0.999, -0.224] | -0.105 | INSUFFICIENT_SAMPLE |
| btc_lead | 8 | -0.609 | [-1.405, 0.585] | -0.221 | INSUFFICIENT_SAMPLE |
| support_bounce | 53 | -0.103 | [-0.658, 0.499] | 0.053 | INSUFFICIENT_SAMPLE |
| swing_breakout | 98 | -0.126 | [-0.577, 0.367] | 0.017 | INSUFFICIENT_SAMPLE |
| steady_scalper | 229 | -0.186 | [-0.323, -0.055] | -0.064 | FAILED_OOS |
| zone_rejection | 6 | -0.58 | [-1.311, 1.309] | -0.343 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 68 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 68, 'mean_difference_R': 0.038, 'ci_low': -0.204, 'ci_high': 0.266, 'atr_exp_R': -0.511, 'chart_exp_R': -0.473}

Baseline (1h trend, one trade a day) OOS: {'trades': 64, 'win_rate': 0.438, 'avg_win_R': 1.351, 'avg_loss_R': -1.282, 'gross_expectancy_R': 0.254, 'net_expectancy_R': -0.13, 'cost_per_trade_R': 0.384, 'total_net_R': -8.32, 'profit_factor': 0.82, 'max_drawdown_R': 14.05, 'longest_losing_streak': 6, 't_stat': -0.73, 'ci_level': 0.9996, 'ci_low': -0.62, 'ci_high': 0.53}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.