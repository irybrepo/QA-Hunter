import html
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from config import (
    MAX_DAYS_OLD,
    QA_KEYWORDS,
    EXCLUDE_TITLE_KEYWORDS,
    BLOCKED_LOCATIONS,
    PRIORITY_KEYWORDS,
    UA_NATIVE_SOURCES
)

REMOTE_POSITIVE_MARKERS = [
    "remote", "worldwide", "anywhere", "work from home",
    "wfh", "distributed", "global", "ukraine", "emea", "europe"
]

NON_REMOTE_MARKERS = [
    "hybrid", "on-site", "onsite", "in-office", "office-first", "office based"
]


def _parse_date(date_val):
    if not date_val:
        return None

    date_str = str(date_val).strip()

    # 1. Unix timestamp (seconds or milliseconds)
    if date_str.isdigit():
        ts = int(date_str)
        if ts > 1e11:
            ts = ts / 1000.0
        return datetime.fromtimestamp(ts, tz=timezone.utc)

    # 2. ISO 8601 format (e.g., 2026-11-13T08:00:21+00:00)
    try:
        clean_iso = date_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean_iso)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        pass

    # 3. RFC 2822 RSS format (e.g., Tue, 17 Nov 2026 10:00:00 +0000)
    try:
        dt = parsedate_to_datetime(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (TypeError, ValueError):
        return None


def _is_qa_title(title_lower):
    if any(bad in title_lower for bad in EXCLUDE_TITLE_KEYWORDS):
        return False

    for kw in QA_KEYWORDS:
        pattern = r"\b" + re.escape(kw) + r"\b"
        if re.search(pattern, title_lower):
            return True
    return False


def _is_ua_remote_accessible(job):
    source = job.get("source", "")
    if source in UA_NATIVE_SOURCES:
        return True

    title_lower = (job.get("title") or "").lower()
    location = (job.get("location") or job.get("candidate_required_location") or "").lower()
    description = (job.get("description") or "").lower()
    header_text = f"{title_lower} {location}"

    # 1. Reject explicit office or hybrid roles
    if any(marker in header_text for marker in NON_REMOTE_MARKERS):
        return False

    # 2. Require explicit remote/worldwide/regional indicator in title or location
    has_remote_marker = any(marker in header_text for marker in REMOTE_POSITIVE_MARKERS)
    if not has_remote_marker:
        return False

    # 3. Check strict country/region blocks
    broad_positive = any(m in location for m in ["ukraine", "worldwide", "anywhere", "emea", "europe", "global"])
    combined_text = f"{location} {description}"

    for blocked in BLOCKED_LOCATIONS:
        if blocked in location:
            return False
        if not broad_positive and blocked in combined_text:
            return False

    return True


def filter_qa_jobs(jobs):
    """Filter and prioritize Remote Manual QA jobs accessible from Ukraine within MAX_DAYS_OLD."""
    now = datetime.now(timezone.utc)
    filtered_jobs = []

    for job in jobs:
        title = html.unescape(job.get("title", "")).strip()
        company = html.unescape(job.get("company_name", "")).strip()
        job["title"] = title
        job["company_name"] = company
        title_lower = title.lower()

        if not _is_qa_title(title_lower):
            continue

        dt = _parse_date(job.get("date"))
        if dt is not None:
            days_old = (now - dt).days
            if days_old > MAX_DAYS_OLD or days_old < -1:
                continue
            job["days_old"] = max(0, days_old)
        else:
            job["days_old"] = 99

        if not _is_ua_remote_accessible(job):
            continue

        desc_lower = (job.get("description") or "").lower()
        is_priority = any(pk in title_lower or pk in desc_lower for pk in PRIORITY_KEYWORDS)
        job["is_priority"] = is_priority

        filtered_jobs.append(job)

    filtered_jobs.sort(key=lambda j: (not j.get("is_priority", False), j.get("days_old", 99)))
    return filtered_jobs
