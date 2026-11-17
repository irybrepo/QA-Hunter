import requests


def get_jobs():
    """
    Get jobs from RemoteOK.
    """

    response = requests.get(
        "https://remoteok.com/api"
    )

    data = response.json()

    normalized_jobs = []

    for job in data[1:]:

        normalized_jobs.append({
            "title": job.get("position", ""),
            "company_name": job.get("company", ""),
            "candidate_required_location": job.get("location", ""),
            "url": job.get("url", "")
        })

    return normalized_jobs