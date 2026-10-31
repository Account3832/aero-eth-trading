# Crypto backtest report
**CRYPTO SPOT PRICE-SIGNAL RESEARCH for ADA-USD. Long-only. Paper only.**

Data: ADA-USD 2024-10-20 00:00:00+00:00 to 2026-10-31 03:30:00+00:00 (742 days). Generated 2026-10-31 03:59:25.970585+00:00.
Entry candles: 15 minutes. Costs assumed: fee 0.1% + slippage 0.05% per side.


| Strategy | OOS trades | OOS net exp (R) | OOS CI | Break-even fee (%/side) | Verdict |
|---|---|---|---|---|---|
| trend_pullback | 172 | -0.343 | [-0.633, -0.031] | -0.042 | FAILED_OOS |
| donchian_breakout | 77 | -0.299 | [-0.71, 0.159] | -0.072 | INSUFFICIENT_SAMPLE |
| squeeze_breakout | 32 | -0.774 | [-1.259, -0.188] | -0.16 | INSUFFICIENT_SAMPLE |
| oversold_bounce | 16 | -0.58 | [-1.205, 0.31] | -0.141 | INSUFFICIENT_SAMPLE |
| range_bounce | 81 | -0.601 | [-0.961, -0.239] | -0.073 | INSUFFICIENT_SAMPLE |
| btc_lead | 9 | -0.35 | [-1.381, 0.859] | -0.001 | INSUFFICIENT_SAMPLE |
| support_bounce | 43 | -0.601 | [-1.124, 0.08] | -0.092 | INSUFFICIENT_SAMPLE |
| swing_breakout | 97 | -0.481 | [-0.867, 0.012] | -0.156 | INSUFFICIENT_SAMPLE |
| steady_scalper | 197 | -0.241 | [-0.388, -0.085] | -0.065 | FAILED_OOS |
| zone_rejection | 2 | -1.327 | [-1.432, -1.222] | -0.407 | INSUFFICIENT_SAMPLE |

## Chart-based exits vs fixed exits (same entries)
Verdict: **INSUFFICIENT_SAMPLE** - only 77 paired out-of-sample trades; at least 100 are needed
Pooled out-of-sample: {'paired_trades': 77, 'mean_difference_R': 0.157, 'ci_low': -0.032, 'ci_high': 0.379, 'atr_exp_R': -0.267, 'chart_exp_R': -0.111}

Baseline (1h trend, one trade a day) OOS: {'trades': 61, 'win_rate': 0.443, 'avg_win_R': 1.139, 'avg_loss_R': -1.379, 'gross_expectancy_R': 0.165, 'net_expectancy_R': -0.265, 'cost_per_trade_R': 0.429, 'total_net_R': -16.14, 'profit_factor': 0.66, 'max_drawdown_R': 15.87, 'longest_losing_streak': 5, 't_stat': -1.53, 'ci_level': 0.9996, 'ci_low': -0.786, 'ci_high': 0.251}

Limitations:
- Bootstrap CIs ignore serial correlation between trades.
- AERO trades mainly on the Aerodrome DEX on Base; this uses the Coinbase AERO-USD price as a stand-in, so real DEX costs and slippage can differ.
- Slippage per coin is an assumption (smaller or thinner coins get a larger number). Real fills can be worse, especially in fast markets.
- Only one market regime may be covered; crypto cycles are long.
- Past results do not predict future results.