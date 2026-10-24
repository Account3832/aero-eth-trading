# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for AERO-USD. Long-only. Paper only.**

Data: AERO-USD 2024-10-18 00:00:00+00:00 to 2026-10-24 03:30:00+00:00 (737 days). Generated 2026-10-24 03:50:04.690437+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.1% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 210 | -0.193 | [-0.476, 0.125] | -0.0 | NOT_DEMONSTRATED |
| donchian_breakout | 88 | -0.328 | [-0.75, 0.175] | -0.136 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 40 | -0.552 | [-1.093, 0.216] | -0.104 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 24 | -0.539 | [-1.188, 0.184] | -0.152 | INSUFFICIENT_SAMPLE |
| range_bounce | 91 | -0.64 | [-1.0, -0.257] | -0.105 | INSUFFICIENT_SAMPLE |
| btc_lead | 9 | -0.4 | [-1.338, 0.803] | -0.107 | INSUFFICIENT_SAMPLE |
| support_bounce | 51 | -0.08 | [-0.672, 0.481] | 0.063 | INSUFFICIENT_SAMPLE |
| swing_breakout | 97 | -0.078 | [-0.522, 0.461] | 0.048 | INSUFFICIENT_SAMPLE |
| steady_scalper | 232 | -0.181 | [-0.305, -0.063] | -0.061 | FAILED_OOS |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 73 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 73, 'mean_difference_R': 0.06, 'ci_low': -0.174, 'ci_high': 0.291, 'atr_exp_R': -0.517, 'chart_exp_R': -0.457}

Baseline (1h trend, one trade a day) OOS: {'trades': 66, 'win_rate': 0.439, 'avg_win_R': 1.325, 'avg_loss_R': -1.279, 'gross_expectancy_R': 0.245, 'net_expectancy_R': -0.135, 'cost_per_trade_R': 0.379, 'total_net_R': -8.88, 'profit_factor': 0.81, 'max_drawdown_R': 14.05, 'longest_losing_streak': 6, 't_stat': -0.78, 'ci_level': 0.9995, 'ci_low': -0.724, 'ci_high': 0.464}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.