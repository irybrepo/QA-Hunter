import requests
from bs4 import BeautifulSoup


def get_jobs():
    base_url = "https://workingnomads.com"
    api_url = f"{base_url}/api/exposed_jobs/"
    jobs = []

    session = requests.Session()
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"{base_url}/jobs",
        "X-Requested-With": "XMLHttpRequest",
    }

    session.get(f"{base_url}/jobs", headers=headers, timeout=15)
    response = session.get(api_url, headers=headers, timeout=15)
    response.raise_for_status()

    text = response.text.strip()
    if text.startswith("["):
        data = response.json()
        for item in data:
            title = (item.get("title") or "").strip()
            company = (item.get("company_name") or "Working Nomads Employer").strip()
            location = (item.get("location") or "Worldwide").strip()
            link = (item.get("url") or "").strip()
            pub_date = (item.get("pub_date") or "").strip()
            description = (item.get("description") or "").strip()

            jobs.append({
                "title": title,
                "company_name": company,
                "location": f"Remote ({location})" if location else "Remote",
                "url": link,
                "source": "Working Nomads",
                "posted_at": pub_date,
                "description": description,
                "remote": True,
            })
        return jobs

    # Fallback: parse HTML job listings if JSON API is restricted
    soup = BeautifulSoup(text, "html.parser")
    for link_tag in soup.find_all("a", href=True):
        href = link_tag["href"]
        if "/jobs/" not in href or href.rstrip("/").endswith("/jobs"):
            continue
        title = " ".join(link_tag.get_text(" ", strip=True).split())
        if not title or len(title) < 4:
            continue
        full_url = href if href.startswith("http") else f"{base_url}{href}"
        if any(j["url"] == full_url for j in jobs):
            continue

        jobs.append({
            "title": title,
            "company_name": "Working Nomads Employer",
            "location": "Remote",
            "url": full_url,
            "source": "Working Nomads",
            "posted_at": "",
            "description": title,
            "remote": True,
        })

    return jobs
