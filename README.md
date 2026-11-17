# QA Hunter

An open-source Python tool that aggregates remote **Manual QA** job openings accessible from Ukraine across 7 Ukrainian and international platforms, normalizes data, removes duplicates, and filters out automation-only or office-based roles.

## Features
- **Multi-source aggregation (7 sources):** Fetches live vacancies from Ukrainian job boards (**Djinni**, **DOU**) and global remote APIs/feeds (**Remotive**, **RemoteOK**, **Jobicy**, **Arbeitnow**, **Himalayas**).
- **Data normalization:** Unifies different RSS feeds, HTML pages, and JSON API schemas into a single clean format.
- **Smart QA & Remote filtering:** Targets Manual QA, Mobile QA, and Software Tester roles posted within the last 14 days while excluding SDET/Automation positions, non-remote office roles, and strict geo-blocked vacancies.
- **Priority ranking:** Boosts Mobile (iOS/Android) and Manual QA roles to the top of the output.
- **Deduplication:** Removes duplicate job postings across sources.

## Project Structure
```text
QA_Hunter/
├── main.py              # Entry point and pipeline orchestration
├── config.py            # Keywords, headers, geo-blocks, and filter settings
├── requirements.txt     # Project dependencies
├── sources/
│   ├── djinni.py        # Djinni web scraper
│   ├── dou.py           # DOU RSS feed parser
│   ├── remotive.py      # Remotive API integration
│   ├── remoteok.py      # RemoteOK API integration
│   ├── jobicy.py        # Jobicy RSS feed parser
│   ├── arbeitnow.py     # Arbeitnow API integration
│   └── himalayas.py     # Himalayas API integration
└── filters/
    ├── qa_filter.py     # Keyword, remote-only, geo, and freshness filtering
    └── deduplicate.py   # Duplicate removal logic
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
