import cloudscraper
from bs4 import BeautifulSoup


def get_jobs():
    url = "https://weworkremotely.com"
    jobs = []

    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "darwin",
            "desktop": True,
        }
    )

    response = scraper.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for link_tag in soup.select('a[href^="/remote-jobs/"]'):
        href = link_tag.get("href", "")
        if "/search" in href or href == "/remote-jobs/":
            continue

        title_el = link_tag.select_one("h3, .title, [class*='title']")
        company_el = link_tag.select_one(".company, [class*='company']")

        title = title_el.get_text(strip=True) if title_el else link_tag.get_text(" ", strip=True)
        company = company_el.get_text(strip=True) if company_el else "We Work Remotely Employer"

        if not title or len(title) < 4:
            continue

        full_url = f"https://weworkremotely.com{href}"
        jobs.append({
            "title": title,
            "company_name": company,
            "location": "Remote",
            "url": full_url,
            "source": "We Work Remotely",
            "posted_at": "",
            "description": title,
            "remote": True,
        })

    # Remove duplicates by URL
    unique_jobs = list({job["url"]: job for job in jobs}.values())
    return unique_jobs
