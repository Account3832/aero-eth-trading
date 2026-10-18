# Status
- Built and unit-tested on synthetic data (17 tests). Real-data results are unknown until you run the Research job.
- No strategy is proven. Verdicts: NOT_DEMONSTRATED, INSUFFICIENT_SAMPLE (<100 fair-test trades), FAILED_OOS, EDGE_SUPPORTED.
- Fair test = last 25% of history, reported once, Bonferroni-adjusted confidence interval, costs included.
