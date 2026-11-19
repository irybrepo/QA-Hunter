import requests
from bs4 import BeautifulSoup
from config import HEADERS


def get_jobs():
    url = "https://thelobbyx.com"
    jobs = []

    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")


    for article in soup.find_all(["article", "div"], class_=lambda c: c and ("post" in c or "vacanc" in c or "card" in c)):
        link_tag = article.find("a", href=True)
        if not link_tag:
            continue

        href = link_tag["href"]
        if "/category/" in href or "/page/" in href or href.rstrip("/") == "https://thelobbyx.com":
            continue

        title_tag = article.find(["h2", "h3", "h4"])
        title = title_tag.get_text(" ", strip=True) if title_tag else link_tag.get_text(" ", strip=True)
        title = " ".join(title.split())

        if not title or len(title) < 4:
            continue

        full_url = href if href.startswith("http") else f"https://thelobbyx.com{href}"
        if any(j["url"] == full_url for j in jobs):
            continue

        full_card_text = " ".join(article.get_text(" ", strip=True).split())

        jobs.append({
            "title": title,
            "company_name": "Lobby X Partner",
            "location": "Ukraine / Remote",
            "url": full_url,
            "source": "Lobby X",
            "posted_at": "",
            "description": full_card_text,
            "remote": "remote" in full_card_text.lower() or "віддалено" in full_card_text.lower(),
        })

    return jobs
