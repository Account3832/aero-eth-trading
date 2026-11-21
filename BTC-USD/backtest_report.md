# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for BTC-USD. Long-only. Paper only.**

Data: BTC-USD 2024-10-18 00:00:00+00:00 to 2026-11-21 10:45:00+00:00 (765 days). Generated 2026-11-21 11:13:46.059977+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.02% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 193 | -0.82 | [-1.106, -0.47] | -0.028 | FAILED_OOS |
| donchian_breakout | 88 | -0.6 | [-1.034, -0.034] | -0.025 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 56 | -0.827 | [-1.49, -0.242] | 0.0 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 31 | -0.788 | [-1.249, -0.244] | -0.051 | INSUFFICIENT_SAMPLE |
| range_bounce | 76 | -1.014 | [-1.524, -0.578] | -0.015 | INSUFFICIENT_SAMPLE |
| btc_lead | 0 | n/a | n/a | n/a | INSUFFICIENT_SAMPLE |
| support_bounce | 68 | -0.965 | [-1.561, -0.326] | -0.012 | INSUFFICIENT_SAMPLE |
| swing_breakout | 94 | -0.637 | [-1.049, -0.224] | -0.037 | INSUFFICIENT_SAMPLE |
| steady_scalper | 226 | -0.539 | [-0.688, -0.38] | -0.039 | FAILED_OOS |
| zone_rejection | 6 | -1.414 | [-2.212, 0.171] | -0.107 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 68 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 68, 'mean_difference_R': -0.018, 'ci_low': -0.206, 'ci_high': 0.177, 'atr_exp_R': -0.836, 'chart_exp_R': -0.853}

Baseline (1h trend, one trade a day) OOS: {'trades': 66, 'win_rate': 0.288, 'avg_win_R': 1.012, 'avg_loss_R': -1.696, 'gross_expectancy_R': -0.05, 'net_expectancy_R': -0.916, 'cost_per_trade_R': 0.866, 'total_net_R': -60.48, 'profit_factor': 0.24, 'max_drawdown_R': 59.07, 'longest_losing_streak': 8, 't_stat': -5.44, 'ci_level': 0.9996, 'ci_low': -1.44, 'ci_high': -0.314}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.