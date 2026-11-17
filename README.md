# QA Hunter

An open-source Python tool that aggregates remote **Manual QA** job openings from public APIs, normalizes the data, removes duplicates, and filters out automation-only or geo-restricted roles.

## Features
- **Multi-source aggregation:** Fetches live remote vacancies from Remotive and RemoteOK APIs.
- **Data normalization:** Unifies different API schemas into a single clean format.
- **Smart QA filtering:** Targets Manual QA, QA Engineer, and Software Tester roles while excluding SDET/Automation positions.
- **Deduplication:** Removes duplicate job postings across sources.

## Project Structure
```text
QA_Hunter/
├── main.py              # Entry point and pipeline orchestration
├── config.py            # Keywords, headers, and filter settings
├── requirements.txt     # Project dependencies
├── sources/
│   ├── remotive.py      # Remotive API integration
│   └── remoteok.py      # RemoteOK API integration
└── filters/
    ├── qa_filter.py     # Keyword, location, and freshness filtering
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
