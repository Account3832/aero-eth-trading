# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for ETH-USD. Long-only. Paper only.**

Data: ETH-USD 2024-10-18 00:00:00+00:00 to 2026-11-21 10:45:00+00:00 (765 days). Generated 2026-11-21 11:13:09.816459+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.03% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 210 | -0.648 | [-0.903, -0.36] | -0.035 | FAILED_OOS |
| donchian_breakout | 68 | -0.439 | [-0.9, 0.113] | -0.024 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 51 | -0.634 | [-1.232, -0.012] | -0.004 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 40 | -0.71 | [-1.199, -0.124] | -0.085 | INSUFFICIENT_SAMPLE |
| range_bounce | 85 | -0.693 | [-1.095, -0.335] | -0.018 | INSUFFICIENT_SAMPLE |
| btc_lead | 4 | -1.158 | [-2.213, 0.995] | -0.066 | INSUFFICIENT_SAMPLE |
| support_bounce | 59 | -0.775 | [-1.275, -0.155] | -0.048 | INSUFFICIENT_SAMPLE |
| swing_breakout | 87 | -0.412 | [-0.847, 0.019] | -0.015 | INSUFFICIENT_SAMPLE |
| steady_scalper | 231 | -0.347 | [-0.474, -0.228] | -0.022 | FAILED_OOS |
| zone_rejection | 6 | -0.57 | [-1.392, 1.305] | -0.113 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 67 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 67, 'mean_difference_R': 0.085, 'ci_low': -0.138, 'ci_high': 0.325, 'atr_exp_R': -0.391, 'chart_exp_R': -0.306}

Baseline (1h trend, one trade a day) OOS: {'trades': 64, 'win_rate': 0.312, 'avg_win_R': 1.262, 'avg_loss_R': -1.559, 'gross_expectancy_R': -0.01, 'net_expectancy_R': -0.677, 'cost_per_trade_R': 0.667, 'total_net_R': -43.35, 'profit_factor': 0.37, 'max_drawdown_R': 43.4, 'longest_losing_streak': 7, 't_stat': -3.86, 'ci_level': 0.9996, 'ci_low': -1.171, 'ci_high': -0.098}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.