# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for ETH-USD. Long-only. Paper only.**

Data: ETH-USD 2024-10-18 00:00:00+00:00 to 2026-11-28 11:30:00+00:00 (772 days). Generated 2026-11-28 11:53:58.617695+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.03% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 217 | -0.646 | [-0.951, -0.348] | -0.036 | FAILED_OOS |
| donchian_breakout | 69 | -0.474 | [-0.959, 0.129] | -0.035 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 54 | -0.613 | [-1.237, 0.024] | -0.004 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 42 | -0.627 | [-1.166, -0.175] | -0.068 | INSUFFICIENT_SAMPLE |
| range_bounce | 87 | -0.667 | [-1.049, -0.284] | -0.015 | INSUFFICIENT_SAMPLE |
| btc_lead | 4 | -1.158 | [-2.213, 0.995] | -0.066 | INSUFFICIENT_SAMPLE |
| support_bounce | 59 | -0.748 | [-1.18, -0.242] | -0.046 | INSUFFICIENT_SAMPLE |
| swing_breakout | 89 | -0.431 | [-0.845, 0.034] | -0.021 | INSUFFICIENT_SAMPLE |
| steady_scalper | 238 | -0.344 | [-0.47, -0.222] | -0.022 | FAILED_OOS |
| zone_rejection | 6 | -0.57 | [-1.392, 1.305] | -0.113 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 67 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 67, 'mean_difference_R': 0.085, 'ci_low': -0.138, 'ci_high': 0.325, 'atr_exp_R': -0.391, 'chart_exp_R': -0.306}

Baseline (1h trend, one trade a day) OOS: {'trades': 68, 'win_rate': 0.294, 'avg_win_R': 1.262, 'avg_loss_R': -1.548, 'gross_expectancy_R': -0.065, 'net_expectancy_R': -0.721, 'cost_per_trade_R': 0.656, 'total_net_R': -49.05, 'profit_factor': 0.34, 'max_drawdown_R': 49.1, 'longest_losing_streak': 8, 't_stat': -4.33, 'ci_level': 0.9996, 'ci_low': -1.247, 'ci_high': -0.135}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.