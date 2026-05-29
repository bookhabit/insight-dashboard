import feedparser

FRAMEWORK = "주체찾기"
SOURCE    = "Indie Hackers"
FEED_URL  = "https://www.indiehackers.com/feed.rss"


def fetch() -> list[dict]:
    feed = feedparser.parse(FEED_URL)
    items = []
    for entry in feed.entries:
        items.append({
            "name":        entry.get("title", ""),
            "description": entry.get("summary", "")[:300],
            "category":    "",
            "source":      SOURCE,
            "framework":   FRAMEWORK,
            "url":         entry.get("link", ""),
            "extra":       {},
        })
    return items
