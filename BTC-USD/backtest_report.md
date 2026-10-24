# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for BTC-USD. Long-only. Paper only.**

Data: BTC-USD 2024-10-18 00:00:00+00:00 to 2026-10-24 03:30:00+00:00 (737 days). Generated 2026-10-24 03:50:11.998754+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.02% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 220 | -0.882 | [-1.142, -0.569] | -0.035 | FAILED_OOS |
| donchian_breakout | 95 | -0.62 | [-0.984, -0.132] | -0.032 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 64 | -0.83 | [-1.372, -0.234] | 0.003 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 32 | -0.755 | [-1.242, -0.216] | -0.042 | INSUFFICIENT_SAMPLE |
| range_bounce | 70 | -1.056 | [-1.652, -0.519] | -0.014 | INSUFFICIENT_SAMPLE |
| btc_lead | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |
| support_bounce | 70 | -0.881 | [-1.404, -0.318] | -0.003 | INSUFFICIENT_SAMPLE |
| swing_breakout | 94 | -0.574 | [-0.957, -0.16] | -0.024 | INSUFFICIENT_SAMPLE |
| steady_scalper | 249 | -0.565 | [-0.705, -0.418] | -0.043 | FAILED_OOS |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 83 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 83, 'mean_difference_R': 0.003, 'ci_low': -0.174, 'ci_high': 0.188, 'atr_exp_R': -0.834, 'chart_exp_R': -0.831}

Baseline (1h trend, one trade a day) OOS: {'trades': 73, 'win_rate': 0.315, 'avg_win_R': 0.99, 'avg_loss_R': -1.698, 'gross_expectancy_R': 0.044, 'net_expectancy_R': -0.851, 'cost_per_trade_R': 0.895, 'total_net_R': -62.12, 'profit_factor': 0.27, 'max_drawdown_R': 61.31, 'longest_losing_streak': 8, 't_stat': -5.23, 'ci_level': 0.9995, 'ci_low': -1.386, 'ci_high': -0.358}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.