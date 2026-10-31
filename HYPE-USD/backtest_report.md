# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for HYPE-USD. Long-only. Paper only.**

Data: HYPE-USD 2026-02-05 19:30:00+00:00 to 2026-10-31 03:30:00+00:00 (269 days). Generated 2026-10-31 03:59:08.668162+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.08% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 68 | -0.603 | [-0.989, -0.119] | -0.114 | INSUFFICIENT_SAMPLE |
| donchian_breakout | 38 | -0.68 | [-1.175, -0.106] | -0.208 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 18 | -0.586 | [-1.43, 0.484] | -0.081 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 10 | -0.598 | [-1.357, 0.422] | -0.151 | INSUFFICIENT_SAMPLE |
| range_bounce | 23 | -0.85 | [-1.449, -0.136] | -0.152 | INSUFFICIENT_SAMPLE |
| btc_lead | 3 | -0.113 | [-1.254, 0.872] | 0.057 | INSUFFICIENT_SAMPLE |
| support_bounce | 22 | -0.286 | [-1.264, 0.696] | 0.012 | INSUFFICIENT_SAMPLE |
| swing_breakout | 34 | -0.56 | [-1.11, 0.128] | -0.146 | INSUFFICIENT_SAMPLE |
| steady_scalper | 79 | -0.349 | [-0.611, -0.099] | -0.099 | INSUFFICIENT_SAMPLE |
| zone_rejection | 2 | -1.207 | [-1.209, -1.204] | -0.717 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 23 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 23, 'mean_difference_R': 0.04, 'ci_low': -0.259, 'ci_high': 0.323, 'atr_exp_R': -0.491, 'chart_exp_R': -0.451}

Baseline (1h trend, one trade a day) OOS: {'trades': 29, 'win_rate': 0.172, 'avg_win_R': 1.973, 'avg_loss_R': -1.406, 'gross_expectancy_R': -0.298, 'net_expectancy_R': -0.824, 'cost_per_trade_R': 0.525, 'total_net_R': -23.89, 'profit_factor': 0.29, 'max_drawdown_R': 25.61, 'longest_losing_streak': 14, 't_stat': -3.38, 'ci_level': 0.9996, 'ci_low': -1.459, 'ci_high': 0.134}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.