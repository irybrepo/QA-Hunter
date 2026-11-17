import requests
from config import HEADERS


def get_jobs():
    """Fetch and normalize remote jobs from Himalayas API."""
    url = "https://himalayas.app" + "/jobs/api?limit=50"
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    data = response.json()

    normalized_jobs = []
    for job in data.get("jobs", []):
        restrictions = job.get("locationRestrictions") or []
        location = ", ".join(restrictions) if restrictions else "Worldwide"

        normalized_jobs.append({
            "title": job.get("title", ""),
            "company_name": job.get("companyName", ""),
            "location": location,
            "url": job.get("applicationLink") or job.get("guid", ""),
            "date": str(job.get("pubDate", "")),
            "description": job.get("description", ""),
            "source": "Himalayas"
        })

    return normalized_jobs
