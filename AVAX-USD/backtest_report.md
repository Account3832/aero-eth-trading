# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for AVAX-USD. Long-only. Paper only.**

Data: AVAX-USD 2024-10-20 00:00:00+00:00 to 2026-10-24 03:30:00+00:00 (735 days). Generated 2026-10-24 03:51:04.311153+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |
| donchian_breakout | 1 | -1.188 | n/a | -0.691 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |
| oversold_bounce | 1 | -0.053 | n/a | -0.132 | INSUFFICIENT_SAMPLE |
| range_bounce | 1 | -1.387 | n/a | -0.348 | INSUFFICIENT_SAMPLE |
| btc_lead | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |
| support_bounce | 1 | -1.382 | n/a | -0.353 | INSUFFICIENT_SAMPLE |
| swing_breakout | 2 | -1.148 | [-1.188, -1.109] | -0.645 | INSUFFICIENT_SAMPLE |
| steady_scalper | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 1 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 1, 'mean_difference_R': 0.035, 'ci_low': nan, 'ci_high': nan, 'atr_exp_R': -1.188, 'chart_exp_R': -1.153}

Baseline (1h trend, one trade a day) OOS: {'trades': 0}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.