# AERO + ETH Trading (paper only)

A practice-trading assistant for **ETH-USD** and **AERO-USD**. It runs 24/7 on GitHub, checks the market about every 5-10 minutes,
and texts your phone through Telegram when a strategy says "buy". **It never places a real order and never touches an exchange.**
BTC is watched only as background (is the whole market rising or falling?).

## Honest warnings
- **No strategy here is proven.** The app replays and fairly tests each one and shows you the truth, including failures.
- **Fees decide everything in crypto.** Many small trades at a typical 0.1% fee per side can eat all profit. Every report has a table showing results at different fee levels and the "break-even fee". If it is lower than what you really pay, that strategy loses.
- **AERO** mostly trades on a decentralized exchange (Aerodrome, Base). This app uses the Coinbase AERO-USD price as a stand-in, so real costs there may be higher.
- Spot only, so **buy-only** (no shorting). Not financial advice.

## Strategies (chosen for how crypto behaves, not copied from stocks; none tuned on data)
| Name | Idea | Status |
|---|---|---|
| trend_pullback | Buy a dip inside a rising 1h and 4h trend | live practice |
| donchian_breakout | Break above the 24-hour high on strong volume (crypto trends persist) | live practice |
| squeeze_breakout | Quiet, tight price range then a breakout (volatility comes in waves) | live practice |
| oversold_bounce | Sharp "liquidation wick" flush, then price reclaims the level | live practice |
| support_bounce | In an uptrend, a dip to the last higher low that gets rejected (classic support) | research only |
| swing_breakout | Strong close above the last swing high on volume (classic resistance break) | research only |
| range_bounce, btc_lead, steady_scalper | Comparison ideas | research only (no practice trades) |

Practice trades are limited: 1 per coin at a time, 2 total, 6 a day per coin, stop trading for the day after losing 2%.

## Chart reading (support, resistance and trends within trends)
The **Levels & Trends** tab reads the chart like a chart technician: trend on four scales (daily, 4-hour, 1-hour, 15-minute), swing highs and lows,
support/resistance zones ranked Strong / Moderate / Weak (more touches, more time scales and more recent = stronger), trendlines, and a plain-English summary
(for example "a pullback inside a larger uptrend"). Every buy alert also says how much room there is before the next resistance zone.
This is information only: it does not block or change practice trades, and nothing about it is proven until the fair test says so.

## Where to get out
Every buy alert gives a stop, two targets and a time limit. There are two ways to set them (`exit_mode` in `config/settings.yaml`):
- `atr` (default): the stop is a fixed multiple of the recent average candle range, the targets are fixed multiples of the risk.
- `chart`: the stop goes just under the nearest support zone and the targets just under the next resistance zones. If there is no sensible chart plan
  (no room before resistance, or the stop would be too wide) the practice trade is passed and you are told why.
Alerts always show the chart-based alternative too. If the trend structure breaks while a practice trade is open you get a "consider getting out" warning
(advice only, it does not close the paper trade). The Reliability test tab compares the two exit styles on identical trades. Keep `atr` until that comparison shows an advantage.

## Setup (about 30 minutes, no coding)
**Step 1. Make the new GitHub project**
1. Go to github.com and sign in. Click the **+** (top right) then **New repository**.
2. Repository name: `aero-eth-trading`. Choose **Public** (needed so the free dashboard can read it). Click **Create repository**.

**Step 2. Upload the files**
1. Unzip `aero-eth-trading.zip` on your computer.
2. In your new repo click **uploading an existing file**. Open the unzipped folder and drag in everything **inside** it (the folders `cryptoai`, `dashboard`, `config`, `scripts`, `tests`, `docs`, `state` and the files like `README.md`, `requirements.txt`). Click **Commit changes**.
3. Folders that start with a dot are hidden and often do not upload. Make these files by hand: click **Add file > Create new file**, type the name **exactly** (typing `/` makes a folder), paste the text from the file of the same name in the zip, click **Commit**:
   - `.github/workflows/evaluate.yml`
   - `.github/workflows/research.yml`
   - `.github/workflows/telegram-test.yml`
   - `.github/workflows/ci.yml`
   - `.streamlit/config.toml`
   - `.gitignore`

**Step 3. Phone alerts (reuse your SPY bot)**
1. Repo > **Settings** > **Secrets and variables** > **Actions** > **New repository secret**.
2. Name `TELEGRAM_BOT_TOKEN`, paste your bot token in the box. Save. (Never type it in chat.)
3. Name `TELEGRAM_CHAT_ID`, paste your chat number. Save.
4. Repo > **Actions** tab > **Telegram test** > **Run workflow**. A message should arrive on your phone. Alerts are labeled "[CRYPTO / PAPER ONLY ...]" so you can tell them from SPY.
5. If Actions asks you to enable workflows, click the green button. Also: Settings > Actions > General > Workflow permissions > **Read and write permissions** > Save.

**Step 4. Load 2 years of data and run the fair test (once)**
1. **Actions** > **Research and ingest** > **Run workflow** > leave 730 > **Run workflow**.
2. Wait. It can take 20-60 minutes. A green check means done. (Red X? Click it and copy me the last red lines.)

**Step 5. Start the 24/7 checker**
1. **Actions** > **Evaluate (paper only, 24/7)** > **Run workflow** once to test. After that it runs by itself every ~5 minutes.
2. GitHub **pauses scheduled jobs after 60 days with no repo activity**. If alerts stop, open Actions and click **Enable workflow**.

**Step 6. The dashboard (free)**
1. Go to share.streamlit.io, sign in with GitHub, **Create app**, pick the repo `aero-eth-trading`, branch `main`, main file `dashboard/app.py`.
2. Click **Advanced settings > Secrets** and paste one line (use YOUR GitHub username):
   `CRYPTOAI_STATE_URL = "https://raw.githubusercontent.com/YOUR-USERNAME/aero-eth-trading/data"`
3. Click **Deploy**.

**To stop everything:** Actions > each workflow > **...** > **Disable workflow**. To pause practice trades only, add a file named `KILL_SWITCH` on the `data` branch.

## Changing settings
Edit `config/settings.yaml` on GitHub (pencil icon). Fee: set `fee_pct` to what your exchange really charges.
