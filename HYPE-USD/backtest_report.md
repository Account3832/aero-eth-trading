# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for HYPE-USD. Long-only. Paper only.**

Data: HYPE-USD 2026-02-05 19:30:00+00:00 to 2026-11-28 11:30:00+00:00 (297 days). Generated 2026-11-28 11:55:16.894446+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.08% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 61 | -0.498 | [-0.969, 0.097] | -0.081 | INSUFFICIENT_SAMPLE |
| donchian_breakout | 33 | -0.499 | [-1.051, 0.236] | -0.134 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 15 | -0.73 | [-1.513, 0.224] | -0.123 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 12 | -0.725 | [-1.33, 0.134] | -0.225 | INSUFFICIENT_SAMPLE |
| range_bounce | 46 | -0.67 | [-1.149, -0.194] | -0.121 | INSUFFICIENT_SAMPLE |
| btc_lead | 2 | -0.191 | [-1.254, 0.872] | 0.008 | INSUFFICIENT_SAMPLE |
| support_bounce | 19 | -0.503 | [-1.452, 0.678] | -0.051 | INSUFFICIENT_SAMPLE |
| swing_breakout | 33 | -0.451 | [-1.05, 0.319] | -0.096 | INSUFFICIENT_SAMPLE |
| steady_scalper | 70 | -0.313 | [-0.588, -0.007] | -0.082 | INSUFFICIENT_SAMPLE |
| zone_rejection | 1 | -1.204 | n/a | -0.725 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 19 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 19, 'mean_difference_R': 0.109, 'ci_low': -0.216, 'ci_high': 0.436, 'atr_exp_R': -0.241, 'chart_exp_R': -0.132}

Baseline (1h trend, one trade a day) OOS: {'trades': 26, 'win_rate': 0.154, 'avg_win_R': 1.65, 'avg_loss_R': -1.388, 'gross_expectancy_R': -0.421, 'net_expectancy_R': -0.921, 'cost_per_trade_R': 0.499, 'total_net_R': -23.93, 'profit_factor': 0.22, 'max_drawdown_R': 26.56, 'longest_losing_streak': 14, 't_stat': -4.04, 'ci_level': 0.9996, 'ci_low': -1.463, 'ci_high': -0.208}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.