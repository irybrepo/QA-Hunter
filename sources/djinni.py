import xml.etree.ElementTree as ET
import requests
from config import HEADERS


def get_jobs():
    """Fetch and normalize QA jobs from Djinni RSS feed."""
    url = "https://djinni.co" + "/jobs/rss/?primary_keyword=QA"
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    normalized_jobs = []

    for item in root.findall("./channel/item"):
        title = item.findtext("title", default="").strip()
        link = item.findtext("link", default="").strip()
        pub_date = item.findtext("pubDate", default="").strip()
        description = item.findtext("description", default="").strip()

        company = "Djinni Employer"
        if " at " in title:
            parts = title.rsplit(" at ", 1)
            title, company = parts[0].strip(), parts[1].strip()

        normalized_jobs.append({
            "title": title,
            "company_name": company,
            "location": "Ukraine / Remote",
            "url": link,
            "date": pub_date,
            "description": description,
            "source": "Djinni"
        })

    return normalized_jobs
