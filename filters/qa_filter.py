def filter_qa_jobs(jobs):
    """
    Filter Manual QA related jobs.
    """

    keywords = [
        "qa",
        "quality assurance",
        "manual qa",
        "qa engineer",
        "qa analyst",
        "software tester",
        "test engineer",
        "manual tester",
        "mobile tester",
        "web tester",
        "qa manual",
        "tester",
        "quality engineer"
    ]

    exclude_keywords = [
        "automation",
        "sdet",
        "test automation",
        "qa automation",
        "automation engineer"
    ]

    filtered_jobs = []

    for job in jobs:

        title = job.get("title", "").strip().lower()

        # исключаем вакансии по автоматизации
        if any(word in title for word in exclude_keywords):
            continue

        # оставляем QA вакансии
        if any(word in title for word in keywords):
            filtered_jobs.append(job)

    return filtered_jobs