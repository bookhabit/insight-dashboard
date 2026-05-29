from crawler.base import fetch as base_fetch
from config import REDDIT_NICHE

FRAMEWORK = "시장쪼개기"


def fetch() -> list[dict]:
    items = []
    for sub in REDDIT_NICHE:
        url = f"https://www.reddit.com/r/{sub}/hot.json"
        res = base_fetch(url, params={"limit": 25})
        if not res:
            continue
        for post in res.json().get("data", {}).get("children", []):
            d = post.get("data", {})
            if d.get("is_self") and not d.get("selftext"):
                continue
            items.append({
                "name":        d.get("title", "")[:200],
                "description": (d.get("selftext", "") or "")[:300],
                "category":    sub,
                "source":      f"Reddit r/{sub}",
                "framework":   FRAMEWORK,
                "url":         f"https://reddit.com{d.get('permalink', '')}",
                "extra":       {
                    "score":    d.get("score", 0),
                    "comments": d.get("num_comments", 0),
                    "subreddit": sub,
                },
            })
    return items
