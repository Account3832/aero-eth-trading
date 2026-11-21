# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for SOL-USD. Long-only. Paper only.**

Data: SOL-USD 2024-10-20 00:00:00+00:00 to 2026-11-21 10:45:00+00:00 (763 days). Generated 2026-11-21 11:14:29.859842+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 189 | -0.566 | [-0.885, -0.225] | -0.06 | FAILED_OOS |
| donchian_breakout | 76 | -0.257 | [-0.699, 0.247] | -0.001 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 54 | -0.57 | [-1.115, 0.013] | -0.034 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 36 | -0.715 | [-1.111, -0.243] | -0.133 | INSUFFICIENT_SAMPLE |
| range_bounce | 89 | -0.793 | [-1.143, -0.409] | -0.062 | INSUFFICIENT_SAMPLE |
| btc_lead | 7 | -0.899 | [-2.043, 0.176] | -0.103 | INSUFFICIENT_SAMPLE |
| support_bounce | 49 | -0.749 | [-1.339, -0.128] | -0.088 | INSUFFICIENT_SAMPLE |
| swing_breakout | 82 | -0.292 | [-0.767, 0.206] | -0.011 | INSUFFICIENT_SAMPLE |
| steady_scalper | 214 | -0.428 | [-0.597, -0.274] | -0.101 | FAILED_OOS |
| zone_rejection | 3 | -0.437 | [-1.253, 0.894] | -0.089 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 65 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 65, 'mean_difference_R': 0.139, 'ci_low': -0.101, 'ci_high': 0.367, 'atr_exp_R': -0.735, 'chart_exp_R': -0.596}

Baseline (1h trend, one trade a day) OOS: {'trades': 67, 'win_rate': 0.403, 'avg_win_R': 0.946, 'avg_loss_R': -1.517, 'gross_expectancy_R': 0.058, 'net_expectancy_R': -0.524, 'cost_per_trade_R': 0.582, 'total_net_R': -35.13, 'profit_factor': 0.42, 'max_drawdown_R': 34.33, 'longest_losing_streak': 5, 't_stat': -3.27, 'ci_level': 0.9996, 'ci_low': -1.022, 'ci_high': 0.03}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.