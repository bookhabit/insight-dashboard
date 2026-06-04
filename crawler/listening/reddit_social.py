import feedparser
from config import REDDIT_SOCIAL

FRAMEWORK = "소머즈"


def fetch() -> list[dict]:
    items = []
    for sub in REDDIT_SOCIAL:
        feed = feedparser.parse(f"https://www.reddit.com/r/{sub}/new.rss?limit=25")
        for entry in feed.entries:
            items.append({
                "name":        entry.get("title", "")[:200],
                "description": entry.get("summary", "")[:300],
                "category":    "커뮤니티 반응",
                "source":      f"Reddit r/{sub}",
                "framework":   FRAMEWORK,
                "url":         entry.get("link", ""),
                "extra":       {"subreddit": sub},
            })
    return items
