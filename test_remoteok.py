from sources.remoteok import get_jobs


jobs = get_jobs()

print(len(jobs))
print(jobs[0])