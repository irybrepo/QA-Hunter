import requests
from config import HEADERS


def get_jobs():
    """Fetch and normalize remote jobs from Remotive API."""
    url = "https://remotive.com" + "/api/remote-jobs"
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    data = response.json()

    normalized_jobs = []
    for job in data.get("jobs", []):
        normalized_jobs.append({
            "title": job.get("title", ""),
            "company_name": job.get("company_name", ""),
            "location": job.get("candidate_required_location", "") or "Worldwide",
            "url": job.get("url", ""),
            "date": job.get("publication_date", ""),
            "description": job.get("description", ""),
            "source": "Remotive"
        })

    return normalized_jobs
