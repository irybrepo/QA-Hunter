from sources.djinni import get_jobs as get_djinni_jobs
from sources.dou import get_jobs as get_dou_jobs
from sources.remotive import get_jobs as get_remotive_jobs
from sources.remoteok import get_jobs as get_remoteok_jobs
from sources.jobicy import get_jobs as get_jobicy_jobs
from sources.arbeitnow import get_jobs as get_arbeitnow_jobs
from sources.himalayas import get_jobs as get_himalayas_jobs

from filters.qa_filter import filter_qa_jobs
from filters.deduplicate import remove_duplicates


def fetch_safely(source_name, fetch_func):
    try:
        jobs = fetch_func()
        print(f"[OK] {source_name}: {len(jobs)} jobs")
        return jobs
    except Exception as e:
        print(f"[ERROR] {source_name}: {e}")
        return []


def main():
    sources = [
        ("Djinni", get_djinni_jobs),
        ("DOU", get_dou_jobs),
        ("Remotive", get_remotive_jobs),
        ("RemoteOK", get_remoteok_jobs),
        ("Jobicy", get_jobicy_jobs),
        ("Arbeitnow", get_arbeitnow_jobs),
        ("Himalayas", get_himalayas_jobs),
    ]

    all_jobs = []
    for name, func in sources:
        all_jobs += fetch_safely(name, func)

    unique_jobs = remove_duplicates(all_jobs)
    qa_jobs = filter_qa_jobs(unique_jobs)

    print("-" * 60)
    print(f"Total unique jobs fetched: {len(unique_jobs)}")
    print(f"Relevant Manual QA jobs (<= 14 days, UA-friendly): {len(qa_jobs)}")

    for job in qa_jobs:
        print("=" * 60)
        tag = "[MOBILE/MANUAL]" if job.get("is_priority") else "[QA]"
        days = job.get("days_old")
        age_str = f"{days}d ago" if days is not None and days != 99 else "Recent"
        print(f"{tag} [{job.get('source')}] {job.get('title')} @ {job.get('company_name')} ({age_str})")
        loc = job.get("location") or "Worldwide"
        print(f"Location: {loc}")
        print(f"Apply:    {job.get('url')}")


if __name__ == "__main__":
    main()
