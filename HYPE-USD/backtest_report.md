# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for HYPE-USD. Long-only. Paper only.**

Data: HYPE-USD 2026-02-05 19:30:00+00:00 to 2026-11-21 10:45:00+00:00 (290 days). Generated 2026-11-21 11:14:41.454371+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.08% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 53 | -0.611 | [-1.107, -0.043] | -0.114 | INSUFFICIENT_SAMPLE |
| donchian_breakout | 32 | -0.717 | [-1.211, -0.041] | -0.231 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 13 | -0.778 | [-1.523, 0.279] | -0.126 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 9 | -0.773 | [-1.341, 0.127] | -0.227 | INSUFFICIENT_SAMPLE |
| range_bounce | 42 | -0.695 | [-1.187, -0.167] | -0.117 | INSUFFICIENT_SAMPLE |
| btc_lead | 2 | -0.191 | [-1.254, 0.872] | 0.008 | INSUFFICIENT_SAMPLE |
| support_bounce | 18 | -0.46 | [-1.436, 0.725] | -0.035 | INSUFFICIENT_SAMPLE |
| swing_breakout | 32 | -0.588 | [-1.183, 0.294] | -0.152 | INSUFFICIENT_SAMPLE |
| steady_scalper | 61 | -0.395 | [-0.658, -0.109] | -0.122 | INSUFFICIENT_SAMPLE |
| zone_rejection | 1 | -1.204 | n/a | -0.725 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 20 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 20, 'mean_difference_R': 0.087, 'ci_low': -0.237, 'ci_high': 0.406, 'atr_exp_R': -0.545, 'chart_exp_R': -0.458}

Baseline (1h trend, one trade a day) OOS: {'trades': 24, 'win_rate': 0.167, 'avg_win_R': 1.65, 'avg_loss_R': -1.392, 'gross_expectancy_R': -0.381, 'net_expectancy_R': -0.885, 'cost_per_trade_R': 0.503, 'total_net_R': -21.23, 'profit_factor': 0.24, 'max_drawdown_R': 22.5, 'longest_losing_streak': 14, 't_stat': -3.6, 'ci_level': 0.9996, 'ci_low': -1.449, 'ci_high': 0.217}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.