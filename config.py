HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

MAX_DAYS_OLD = 14

QA_KEYWORDS = [
    "qa", "quality assurance", "manual qa", "qa engineer",
    "qa analyst", "software tester", "test engineer",
    "manual tester", "mobile tester", "web tester",
    "qa manual", "tester", "quality engineer", "тестувальник", "тестировщик"
]

# Excluded only if explicitly present in the job title
EXCLUDE_TITLE_KEYWORDS = [
    "automation", "sdet", "aqa", "test automation",
    "qa automation", "automation engineer", "performance engineer",
    "load testing", "security engineer", "penetration"
]

# Strict geo-restrictions blocking candidates from Ukraine
BLOCKED_LOCATIONS = [
    "usa only", "us only", "united states only", "u.s. only",
    "must reside in the us", "must reside in the united states",
    "authorized to work in the united states", "authorized to work in the us",
    "uk only", "united kingdom only", "canada only",
    "must reside in the philippines", "philippines only",
    "latam only", "latin america only", "brazil only", "india only",
    "outside ukraine", "outside russia, belarus, and ukraine"
]

# Keywords used to boost Mobile and Manual QA roles to the top
PRIORITY_KEYWORDS = [
    "mobile", "ios", "android", "manual"
]

# Sources natively targeting the Ukrainian market (all remote roles allowed)
UA_NATIVE_SOURCES = {"Djinni", "DOU"}
