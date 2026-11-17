from sources.remotive import get_jobs as get_remotive_jobs
from sources.remoteok import get_jobs as get_remoteok_jobs
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
    all_jobs = []
    all_jobs += fetch_safely("Remotive", get_remotive_jobs)
    all_jobs += fetch_safely("RemoteOK", get_remoteok_jobs)

    unique_jobs = remove_duplicates(all_jobs)
    qa_jobs = filter_qa_jobs(unique_jobs)

    print("-" * 50)
    print(f"Total unique jobs: {len(unique_jobs)}")
    print(f"Relevant Manual QA jobs found: {len(qa_jobs)}")

    for job in qa_jobs:
        print("=" * 50)
        print(f"[{job.get('source', 'API')}] {job.get('title')} @ {job.get('company_name')}")
        loc = job.get('location') or job.get('candidate_required_location', 'Worldwide')
        print(f"Location: {loc}")
        print(f"URL: {job.get('url')}")


if __name__ == "__main__":
    main()
