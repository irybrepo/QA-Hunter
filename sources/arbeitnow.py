import requests
from config import HEADERS


def get_jobs():
    """Fetch and normalize jobs from Arbeitnow API."""
    url = "https://arbeitnow.com" + "/api/job-board-api"
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    data = response.json()

    normalized_jobs = []
    for job in data.get("data", []):
        location = job.get("location", "")
        if job.get("remote"):
            location = f"Remote ({location})" if location else "Remote"

        normalized_jobs.append({
            "title": job.get("title", ""),
            "company_name": job.get("company_name", ""),
            "location": location or "Europe",
            "url": job.get("url", ""),
            "date": str(job.get("created_at", "")),
            "description": job.get("description", ""),
            "source": "Arbeitnow"
        })

    return normalized_jobs
