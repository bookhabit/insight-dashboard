import feedparser

FRAMEWORK = "주체찾기"
SOURCE    = "Product Hunt"
FEED_URL  = "https://www.producthunt.com/feed"


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
