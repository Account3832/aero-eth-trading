# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for ETH-USD. Long-only. Paper only.**

Data: ETH-USD 2024-10-18 00:00:00+00:00 to 2026-11-14 10:15:00+00:00 (758 days). Generated 2026-11-14 10:33:22.329965+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.03% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 215 | -0.658 | [-0.935, -0.366] | -0.036 | FAILED_OOS |
| donchian_breakout | 71 | -0.439 | [-0.901, 0.145] | -0.022 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 51 | -0.634 | [-1.232, -0.012] | -0.004 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 40 | -0.71 | [-1.199, -0.124] | -0.085 | INSUFFICIENT_SAMPLE |
| range_bounce | 81 | -0.682 | [-1.111, -0.254] | -0.013 | INSUFFICIENT_SAMPLE |
| btc_lead | 4 | -1.158 | [-2.213, 0.995] | -0.066 | INSUFFICIENT_SAMPLE |
| support_bounce | 61 | -0.805 | [-1.273, -0.217] | -0.054 | INSUFFICIENT_SAMPLE |
| swing_breakout | 89 | -0.453 | [-0.897, 0.044] | -0.024 | INSUFFICIENT_SAMPLE |
| steady_scalper | 236 | -0.364 | [-0.485, -0.222] | -0.027 | FAILED_OOS |
| zone_rejection | 6 | -0.57 | [-1.392, 1.305] | -0.113 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 70 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 70, 'mean_difference_R': 0.032, 'ci_low': -0.213, 'ci_high': 0.286, 'atr_exp_R': -0.4, 'chart_exp_R': -0.367}

Baseline (1h trend, one trade a day) OOS: {'trades': 64, 'win_rate': 0.312, 'avg_win_R': 1.262, 'avg_loss_R': -1.559, 'gross_expectancy_R': -0.01, 'net_expectancy_R': -0.677, 'cost_per_trade_R': 0.667, 'total_net_R': -43.35, 'profit_factor': 0.37, 'max_drawdown_R': 43.4, 'longest_losing_streak': 7, 't_stat': -3.86, 'ci_level': 0.9996, 'ci_low': -1.171, 'ci_high': -0.098}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.