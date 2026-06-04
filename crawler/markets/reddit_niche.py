import feedparser
from config import REDDIT_NICHE

FRAMEWORK = "시장쪼개기"


def fetch() -> list[dict]:
    items = []
    for sub in REDDIT_NICHE:
        feed = feedparser.parse(f"https://www.reddit.com/r/{sub}/hot.rss?limit=25")
        for entry in feed.entries:
            items.append({
                "name":        entry.get("title", "")[:200],
                "description": entry.get("summary", "")[:300],
                "category":    sub,
                "source":      f"Reddit r/{sub}",
                "framework":   FRAMEWORK,
                "url":         entry.get("link", ""),
                "extra":       {"subreddit": sub},
            })
    return items
