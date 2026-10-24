# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for BNB-USD. Long-only. Paper only.**

Data: BNB-USD 2025-10-22 18:45:00+00:00 to 2026-10-24 03:30:00+00:00 (368 days). Generated 2026-10-24 03:50:19.538588+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 106 | -0.907 | [-1.257, -0.508] | -0.049 | FAILED_OOS |
| donchian_breakout | 40 | -0.676 | [-1.317, -0.011] | -0.045 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 23 | -1.019 | [-1.918, -0.101] | -0.024 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 16 | -0.9 | [-1.716, -0.061] | -0.07 | INSUFFICIENT_SAMPLE |
| range_bounce | 41 | -1.182 | [-1.757, -0.631] | -0.049 | INSUFFICIENT_SAMPLE |
| btc_lead | 11 | -0.763 | [-2.215, 0.406] | -0.003 | INSUFFICIENT_SAMPLE |
| support_bounce | 32 | -1.021 | [-1.717, -0.223] | -0.046 | INSUFFICIENT_SAMPLE |
| swing_breakout | 36 | -0.537 | [-1.172, 0.097] | -0.011 | INSUFFICIENT_SAMPLE |
| steady_scalper | 121 | -0.675 | [-0.9, -0.464] | -0.079 | FAILED_OOS |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 47 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 47, 'mean_difference_R': -0.048, 'ci_low': -0.272, 'ci_high': 0.142, 'atr_exp_R': -0.741, 'chart_exp_R': -0.788}

Baseline (1h trend, one trade a day) OOS: {'trades': 39, 'win_rate': 0.308, 'avg_win_R': 0.962, 'avg_loss_R': -1.744, 'gross_expectancy_R': 0.013, 'net_expectancy_R': -0.912, 'cost_per_trade_R': 0.925, 'total_net_R': -35.55, 'profit_factor': 0.25, 'max_drawdown_R': 32.52, 'longest_losing_streak': 5, 't_stat': -4.01, 'ci_level': 0.9995, 'ci_low': -1.507, 'ci_high': -0.195}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.