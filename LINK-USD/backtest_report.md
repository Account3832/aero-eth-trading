# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for LINK-USD. Long-only. Paper only.**

Data: LINK-USD 2024-10-20 00:00:00+00:00 to 2026-11-28 11:30:00+00:00 (770 days). Generated 2026-11-28 11:55:55.685189+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 202 | -0.537 | [-0.789, -0.245] | -0.065 | FAILED_OOS |
| donchian_breakout | 76 | -0.192 | [-0.729, 0.296] | 0.016 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 51 | -0.89 | [-1.326, -0.307] | -0.113 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 26 | -0.505 | [-1.113, 0.231] | -0.078 | INSUFFICIENT_SAMPLE |
| range_bounce | 95 | -0.579 | [-0.926, -0.253] | -0.039 | INSUFFICIENT_SAMPLE |
| btc_lead | 3 | 0.001 | [-1.332, 1.075] | 0.1 | INSUFFICIENT_SAMPLE |
| support_bounce | 58 | -0.419 | [-0.889, 0.158] | -0.019 | INSUFFICIENT_SAMPLE |
| swing_breakout | 94 | -0.298 | [-0.707, 0.206] | -0.019 | INSUFFICIENT_SAMPLE |
| steady_scalper | 237 | -0.405 | [-0.549, -0.272] | -0.11 | FAILED_OOS |
| zone_rejection | 6 | -0.192 | [-1.405, 1.805] | 0.018 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 62 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 62, 'mean_difference_R': 0.001, 'ci_low': -0.233, 'ci_high': 0.244, 'atr_exp_R': -0.271, 'chart_exp_R': -0.27}

Baseline (1h trend, one trade a day) OOS: {'trades': 71, 'win_rate': 0.338, 'avg_win_R': 0.972, 'avg_loss_R': -1.417, 'gross_expectancy_R': -0.08, 'net_expectancy_R': -0.61, 'cost_per_trade_R': 0.529, 'total_net_R': -43.28, 'profit_factor': 0.35, 'max_drawdown_R': 45.06, 'longest_losing_streak': 8, 't_stat': -4.16, 'ci_level': 0.9996, 'ci_low': -1.067, 'ci_high': -0.108}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.