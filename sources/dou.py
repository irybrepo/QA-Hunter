import xml.etree.ElementTree as ET
import requests
from config import HEADERS


def get_jobs():
    """Fetch and normalize QA jobs from DOU RSS feed."""
    url = "https://jobs.dou.ua" + "/vacancies/feeds/?category=QA"
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    normalized_jobs = []

    for item in root.findall("./channel/item"):
        raw_title = item.findtext("title", default="").strip()
        link = item.findtext("link", default="").strip()
        pub_date = item.findtext("pubDate", default="").strip()
        description = item.findtext("description", default="").strip()

        company = "DOU Employer"
        title = raw_title
        if " в " in raw_title:
            parts = raw_title.rsplit(" в ", 1)
            title, company = parts[0].strip(), parts[1].strip()

        normalized_jobs.append({
            "title": title,
            "company_name": company,
            "location": "Ukraine / Remote",
            "url": link,
            "date": pub_date,
            "description": description,
            "source": "DOU"
        })

    return normalized_jobs
