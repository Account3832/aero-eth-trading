# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for HYPE-USD. Long-only. Paper only.**

Data: HYPE-USD 2026-02-05 19:30:00+00:00 to 2026-11-14 10:15:00+00:00 (283 days). Generated 2026-11-14 10:34:58.476820+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.08% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 54 | -0.598 | [-1.102, -0.141] | -0.104 | INSUFFICIENT_SAMPLE |
| donchian_breakout | 34 | -0.763 | [-1.229, -0.155] | -0.239 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 12 | -0.733 | [-1.538, 0.313] | -0.107 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 10 | -0.827 | [-1.347, 0.126] | -0.251 | INSUFFICIENT_SAMPLE |
| range_bounce | 35 | -0.804 | [-1.258, -0.232] | -0.132 | INSUFFICIENT_SAMPLE |
| btc_lead | 2 | -0.191 | [-1.254, 0.872] | 0.008 | INSUFFICIENT_SAMPLE |
| support_bounce | 19 | -0.244 | [-1.148, 0.96] | 0.029 | INSUFFICIENT_SAMPLE |
| swing_breakout | 31 | -0.68 | [-1.255, -0.046] | -0.184 | INSUFFICIENT_SAMPLE |
| steady_scalper | 63 | -0.366 | [-0.655, -0.093] | -0.098 | INSUFFICIENT_SAMPLE |
| zone_rejection | 2 | -1.207 | [-1.209, -1.204] | -0.717 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 21 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 21, 'mean_difference_R': 0.085, 'ci_low': -0.212, 'ci_high': 0.381, 'atr_exp_R': -0.58, 'chart_exp_R': -0.495}

Baseline (1h trend, one trade a day) OOS: {'trades': 26, 'win_rate': 0.192, 'avg_win_R': 1.662, 'avg_loss_R': -1.4, 'gross_expectancy_R': -0.289, 'net_expectancy_R': -0.811, 'cost_per_trade_R': 0.522, 'total_net_R': -21.1, 'profit_factor': 0.28, 'max_drawdown_R': 23.32, 'longest_losing_streak': 14, 't_stat': -3.26, 'ci_level': 0.9996, 'ci_low': -1.444, 'ci_high': 0.091}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.