import os
import warnings
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")

from sources.djinni import get_jobs as get_djinni_jobs
from sources.dou import get_jobs as get_dou_jobs
from sources.remotive import get_jobs as get_remotive_jobs
from sources.remoteok import get_jobs as get_remoteok_jobs
from sources.jobicy import get_jobs as get_jobicy_jobs
from sources.arbeitnow import get_jobs as get_arbeitnow_jobs
from sources.himalayas import get_jobs as get_himalayas_jobs
from sources.weworkremotely import get_jobs as get_weworkremotely_jobs
from sources.workingnomads import get_jobs as get_workingnomads_jobs
from sources.lobbyx import get_jobs as get_lobbyx_jobs

from filters.qa_filter import filter_qa_jobs
from filters.deduplicate import remove_duplicates
from storage.history import load_sent_urls, save_sent_urls
from notifiers.telegram import notify_new_jobs


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
        ("Lobby X", get_lobbyx_jobs),
        ("Remotive", get_remotive_jobs),
        ("RemoteOK", get_remoteok_jobs),
        ("Jobicy", get_jobicy_jobs),
        ("Arbeitnow", get_arbeitnow_jobs),
        ("Himalayas", get_himalayas_jobs),
        ("We Work Remotely", get_weworkremotely_jobs),
        ("Working Nomads", get_workingnomads_jobs),
    ]

    all_jobs = []
    for name, func in sources:
        all_jobs += fetch_safely(name, func)

    unique_jobs = remove_duplicates(all_jobs)
    qa_jobs = filter_qa_jobs(unique_jobs)

    print("-" * 60)
    print(f"Total unique jobs fetched: {len(unique_jobs)}")
    print(f"Relevant Manual QA jobs (<= 14 days, UA-friendly): {len(qa_jobs)}")

    bot_token = os.getenv("TG_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TG_CHAT_ID", "").strip()

    sent_urls = load_sent_urls()
    updated_urls = notify_new_jobs(qa_jobs, bot_token, chat_id, sent_urls)
    save_sent_urls(updated_urls)


if __name__ == "__main__":
    main()
