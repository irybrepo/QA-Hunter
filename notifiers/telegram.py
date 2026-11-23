import html
import re
import time
import requests


UA_SOURCES = {"djinni", "dou", "lobby x", "lobbyx"}


def format_job_message(job):
    source = (job.get("source") or "Unknown").strip()
    source_key = source.lower()
    is_ua = source_key in UA_SOURCES

    title = html.escape(job.get("title") or "QA Engineer")
    company = html.escape(job.get("company_name") or "Unknown Company")
    url = (job.get("url") or "").strip()

    days = job.get("days_old")
    age_str = f"{days}d ago" if days is not None and days != 99 else "Recent"

    if is_ua:
        badge = "🇺🇦 <b>UA REMOTE</b>"
        default_loc = "Ukraine / Remote"
        loc_icon = "📍"
    else:
        badge = "🌍 <b>GLOBAL REMOTE</b>"
        default_loc = "Worldwide / Remote"
        loc_icon = "🗺"

    location = html.escape(job.get("location") or default_loc)
    priority_tag = "🔥 " if job.get("is_priority") else ""

    lines = [
        f"{badge} | {priority_tag}<b>{title}</b>",
        f"🏢 {company}",
        f"{loc_icon} {location} • 🕒 {age_str} • 📌 {html.escape(source)}",
        f"🔗 {html.escape(url)}",
    ]
    return "\n".join(lines)


def notify_new_jobs(jobs, bot_token, chat_id, sent_urls):
    known_urls = set(sent_urls or [])
    new_jobs = []

    for job in jobs:
        url = (job.get("url") or "").strip()
        if url and url not in known_urls:
            new_jobs.append(job)

    if not new_jobs:
        print("[INFO] No new jobs to send to Telegram.")
        return list(known_urls)

    raw_token = "".join((bot_token or "").split())
    match = re.search(r"(\d+:[A-Za-z0-9_-]+)", raw_token)
    clean_token = match.group(1) if match else raw_token
    clean_chat_id = (chat_id or "").strip()

    if not clean_token or not clean_chat_id:
        print("[WARN] TG_BOT_TOKEN or TG_CHAT_ID is missing. Skipping Telegram notifications.")
        return list(known_urls)

    host = "https://api." + "telegram.org"
    api_url = f"{host}/bot{clean_token}/sendMessage"
    sent_count = 0

    for job in new_jobs:
        url = (job.get("url") or "").strip()
        text = format_job_message(job)
        payload = {
            "chat_id": clean_chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }

        try:
            response = requests.post(api_url, json=payload, timeout=15)
            if response.status_code == 200:
                known_urls.add(url)
                sent_count += 1
            else:
                print(f"[ERROR] Telegram API ({response.status_code}): {response.text}")
        except Exception as e:
            print(f"[ERROR] Failed to send Telegram message: {e}")

        time.sleep(1.5)

    print(f"[OK] Sent {sent_count}/{len(new_jobs)} new jobs to Telegram.")
    return list(known_urls)
