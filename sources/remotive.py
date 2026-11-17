import requests
from config import HEADERS


def get_jobs():
    url = "https://remotive.com" + "/api/remote-jobs"
    response = requests.get(url, headers=HEADERS, timeout=15)
    data = response.json()

    normalized_jobs = []
    for job in data.get("jobs", []):
        normalized_jobs.append({
            "title": job.get("title", ""),
            "company_name": job.get("company_name", ""),
            "location": job.get("candidate_required_location", "") or "Worldwide",
            "url": job.get("url", ""),
            "date": job.get("publication_date", ""),
            "source": "Remotive"
        })

    return normalized_jobs
