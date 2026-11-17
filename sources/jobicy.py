import requests
from config import HEADERS


def get_jobs():
    """Fetch and normalize remote jobs from Jobicy API."""
    url = "https://jobicy.com" + "/api/v2/remote-jobs?count=50&tag=qa"
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    data = response.json()

    normalized_jobs = []
    for job in data.get("jobs", []):
        normalized_jobs.append({
            "title": job.get("jobTitle", ""),
            "company_name": job.get("companyName", ""),
            "location": job.get("jobGeo", "") or "Worldwide",
            "url": job.get("url", ""),
            "date": job.get("pubDate", ""),
            "description": job.get("jobDescription", ""),
            "source": "Jobicy"
        })

    return normalized_jobs
