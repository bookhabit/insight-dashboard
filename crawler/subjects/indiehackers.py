import feedparser

FRAMEWORK = "주체찾기"
SOURCE    = "Indie Hackers"

# Indie Hackers 공식 RSS 피드 (그룹별)
FEED_URLS = [
    "https://www.indiehackers.com/group/landing-page-feedback/feed.rss",
    "https://www.indiehackers.com/group/find-a-maker-partner/feed.rss",
    "https://www.indiehackers.com/group/open/feed.rss",
]


def fetch() -> list[dict]:
    items = []
    seen = set()
    for url in FEED_URLS:
        feed = feedparser.parse(url)
        if feed.get("bozo") or not feed.entries:
            continue
        for entry in feed.entries:
            link = entry.get("link", "")
            if not link or link in seen:
                continue
            seen.add(link)
            items.append({
                "name":        entry.get("title", ""),
                "description": entry.get("summary", "")[:300],
                "category":    "",
                "source":      SOURCE,
                "framework":   FRAMEWORK,
                "url":         link,
                "extra":       {},
            })
    return items
