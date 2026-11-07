# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for HYPE-USD. Long-only. Paper only.**

Data: HYPE-USD 2026-02-05 19:30:00+00:00 to 2026-11-07 03:45:00+00:00 (276 days). Generated 2026-11-07 04:06:30.889947+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.08% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 58 | -0.567 | [-1.021, -0.036] | -0.097 | INSUFFICIENT_SAMPLE |
| donchian_breakout | 36 | -0.65 | [-1.175, 0.12] | -0.19 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 12 | -0.733 | [-1.538, 0.313] | -0.107 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 10 | -0.686 | [-1.343, 0.178] | -0.179 | INSUFFICIENT_SAMPLE |
| range_bounce | 27 | -0.788 | [-1.359, -0.189] | -0.133 | INSUFFICIENT_SAMPLE |
| btc_lead | 2 | -0.191 | [-1.254, 0.872] | 0.008 | INSUFFICIENT_SAMPLE |
| support_bounce | 19 | -0.244 | [-1.148, 0.96] | 0.029 | INSUFFICIENT_SAMPLE |
| swing_breakout | 32 | -0.555 | [-1.136, 0.146] | -0.135 | INSUFFICIENT_SAMPLE |
| steady_scalper | 69 | -0.354 | [-0.607, -0.089] | -0.097 | INSUFFICIENT_SAMPLE |
| zone_rejection | 2 | -1.207 | [-1.209, -1.204] | -0.717 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 21 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 21, 'mean_difference_R': 0.085, 'ci_low': -0.212, 'ci_high': 0.381, 'atr_exp_R': -0.58, 'chart_exp_R': -0.495}

Baseline (1h trend, one trade a day) OOS: {'trades': 27, 'win_rate': 0.148, 'avg_win_R': 1.951, 'avg_loss_R': -1.402, 'gross_expectancy_R': -0.375, 'net_expectancy_R': -0.905, 'cost_per_trade_R': 0.531, 'total_net_R': -24.44, 'profit_factor': 0.24, 'max_drawdown_R': 23.32, 'longest_losing_streak': 14, 't_stat': -3.84, 'ci_level': 0.9996, 'ci_low': -1.445, 'ci_high': -0.026}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.