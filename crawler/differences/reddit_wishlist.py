import feedparser
from urllib.parse import urlencode

FRAMEWORK = "한끗차이"
SOURCE    = "Reddit"

QUERIES = [
    "wish there was an app",
    "why is there no app",
    "someone should make an app",
    "app that does",
    "앱이 있으면 좋겠다",
    "이런 앱 없나",
]


def fetch() -> list[dict]:
    items = []
    seen = set()
    for query in QUERIES:
        qs = urlencode({"q": query, "sort": "new", "limit": 15, "type": "link"})
        feed = feedparser.parse(f"https://www.reddit.com/search.rss?{qs}")
        for entry in feed.entries:
            url = entry.get("link", "")
            if url in seen:
                continue
            seen.add(url)
            items.append({
                "name":        entry.get("title", "")[:200],
                "description": entry.get("summary", "")[:300],
                "category":    "앱 개선 수요",
                "source":      f"Reddit (검색: {query})",
                "framework":   FRAMEWORK,
                "url":         url,
                "extra":       {"query": query},
            })
    return items
