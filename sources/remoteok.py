import requests
from config import HEADERS


def get_jobs():
    """Fetch and normalize remote jobs from RemoteOK API."""
    url = "https://remoteok.com" + "/api"
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    data = response.json()

    normalized_jobs = []
    for job in data[1:]:
        normalized_jobs.append({
            "title": job.get("position", ""),
            "company_name": job.get("company", ""),
            "location": job.get("location", "") or "Worldwide",
            "url": job.get("url", ""),
            "date": job.get("date", ""),
            "description": job.get("description", ""),
            "source": "RemoteOK"
        })

    return normalized_jobs
