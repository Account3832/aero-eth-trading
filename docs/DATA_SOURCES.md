# Data sources
- Candles: Coinbase Exchange public API (free, no key): ETH-USD, AERO-USD, BTC-USD, 5-minute, stored as gzip CSV on the `data` branch.
- Backup for the latest ~60 hours: Kraken public API (ETH, BTC only; AERO is not listed there).
- Missing 5-minute slots are filled with a flat candle (volume 0). Candles are used only after they close. All times are UTC.
- No paid data, no API keys.
