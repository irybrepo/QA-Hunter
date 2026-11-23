# 🎯 QA Hunter

Automated job aggregator for **Remote Manual & Mobile QA** positions.  
This tool collects listings from 10 job boards, removes duplicates, filters for relevant remote roles, automatically delivers new job alerts to Telegram every 30 minutes via GitHub Actions.

---

## 📲 Live Telegram Notifications

Newly discovered Remote Manual / Mobile QA roles are automatically posted **every 30 minutes** with zero duplicates in our public Telegram group:

> **[@qahunterapi](https://t.me)**

---

## ✨ Key Features

- **Multi-Source Aggregation:** Parses 10 job boards simultaneously.
- **Smart Deduplication:** Merges cross-posted roles across platforms, tracks previously sent URLs in `storage/sent_jobs.json` to prevent repeat alerts.
- **Targeted QA Filtering:** Focuses on Manual QA, Mobile QA (iOS/Android), QA Engineer, Web QA remote roles posted within 14 days.
- **Automated Cloud Execution:** Runs on a 30-minute schedule (`*/30 * * * *`) via GitHub Actions - works 24/7 without keeping a local machine running.

---

## 🌐 Supported Job Sources

1. **Djinni** (`sources/djinni.py`) - Tech & QA remote positions.
2. **DOU** (`sources/dou.py`) - IT community remote job listings.
3. **Lobby X** (`sources/lobbyx.py`) - Tech, defense, social impact QA openings.
4. **Remotive** (`sources/remotive.py`) - Curated remote tech roles.
5. **RemoteOK** (`sources/remoteok.py`) - Worldwide remote QA listings.
6. **Jobicy** (`sources/jobicy.py`) - Remote-first international opportunities.
7. **Arbeitnow** (`sources/arbeitnow.py`) - European, global remote tech jobs.
8. **Himalayas** (`sources/himalayas.py`) - Remote roles from distributed companies.
9. **We Work Remotely** (`sources/weworkremotely.py`) - Remote software testing, QA positions.
10. **Working Nomads** (`sources/workingnomads.py`) - Curated remote jobs for digital nomads.

---

## 📂 Project Structure

```text
QA-Hunter/
├── .github/
│   └── workflows/
│       └── hunt.yml            # GitHub Actions workflow (runs every 30 minutes)
├── filters/
│   ├── deduplicate.py          # Cross-source duplicate removal
│   └── qa_filter.py            # Role, freshness (<= 14 days), remote filtering
├── notifiers/
│   ├── __init__.py
│   └── telegram.py             # Telegram Bot API formatting, delivery
├── sources/
│   ├── arbeitnow.py            # Arbeitnow parser
│   ├── djinni.py               # Djinni parser
│   ├── dou.py                  # DOU parser
│   ├── himalayas.py            # Himalayas parser
│   ├── jobicy.py               # Jobicy parser
│   ├── lobbyx.py               # Lobby X parser
│   ├── remoteok.py             # RemoteOK parser
│   ├── remotive.py             # Remotive parser
│   ├── weworkremotely.py       # We Work Remotely parser
│   └── workingnomads.py        # Working Nomads parser
├── storage/
│   └── sent_jobs.json          # Persistent history of already sent job URLs
├── main.py                     # Main entry point
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## 🚀 Local Setup & Usage

1. **Clone repository:**
   ```bash
   git clone https://github.com
   cd QA-Hunter
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables (optional, for Telegram alerts):**
   ```bash
   export TG_BOT_TOKEN="your_telegram_bot_token"
   export TG_CHAT_ID="@qahunterapi"
   ```

4. **Run aggregator:**
   ```bash
   python main.py
   ```

---

## ⚙️ GitHub Actions Configuration

To run automated alerts in your own fork:
1. Go to **Settings > Secrets and variables > Actions**, add:
   - `TG_BOT_TOKEN` - Your Telegram Bot API token from `@BotFather`.
   - `TG_CHAT_ID` - Target channel/group username (e.g., `@qahunterapi`), numeric chat ID.
2. Go to **Settings > Actions > General > Workflow permissions**, enable **Read and write permissions** so workflow can commit updates to `storage/sent_jobs.json`.
