import feedparser
from config import NEWS_FEEDS

FRAMEWORK = "소머즈"


def fetch() -> list[dict]:
    items = []
    for feed_cfg in NEWS_FEEDS:
        feed = feedparser.parse(feed_cfg["url"])
        for entry in feed.entries[:20]:
            items.append({
                "name":        entry.get("title", ""),
                "description": entry.get("summary", "")[:300],
                "category":    "뉴스",
                "source":      feed_cfg["name"],
                "framework":   FRAMEWORK,
                "url":         entry.get("link", ""),
                "extra":       {"feed": feed_cfg["name"]},
            })
    return items
