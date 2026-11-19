# QA Hunter

Open-source Python tool that aggregates remote **Manual QA** openings across 10 international job boards and remote platforms, normalizes data, duplicates + filters out office-based roles.

## Features
- **Multi-source aggregation (10 sources):** Fetches live vacancies from major remote APIs, RSS feed (**Djinni**, **DOU**, **Lobby X**, **Remotive**, **RemoteOK**, **Jobicy**, **Arbeitnow**, **Himalayas**, **We Work Remotely**, and **Working Nomads**).
- **Data normalization:** Unifies different RSS feeds, JSON API schemas into single clean format.
- **Smart QA & Remote filtering:** Targets Manual QA, Mobile QA roles posted within the last 14 days while excluding SDET/Automation positions, non-remote office roles.
- **Priority ranking:** Boosts Mobile (iOS/Android) and Manual QA roles to the top of the output.
- **Deduplication:** Removes duplicate job postings across sources.

## Project Structure
```text
QA_Hunter/
├── main.py                  # Entry point and pipeline orchestration
├── config.py                # Keywords, headers, geo-blocks, and filter settings
├── requirements.txt         # Project dependencies
├── sources/
│   ├── djinni.py            # Djinni web scraper
│   ├── dou.py               # DOU RSS feed parser
│   ├── lobbyx.py            # Lobby X IT job board scraper
│   ├── remotive.py          # Remotive API integration
│   ├── remoteok.py          # RemoteOK API integration
│   ├── jobicy.py            # Jobicy RSS feed parser
│   ├── arbeitnow.py         # Arbeitnow API integration
│   ├── himalayas.py         # Himalayas API integration
│   ├── weworkremotely.py    # We Work Remotely scraper
│   └── workingnomads.py     # Working Nomads API/HTML integration
└── filters/
    ├── qa_filter.py         # Keyword, remote-only, geo, and freshness filtering
    └── deduplicate.py       # Duplicate removal logic
```

## Quick Start

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Run the parser:
```bash
python3 main.py
```
