from crawler.base import fetch as base_fetch
from config import REDDIT_SOCIAL

FRAMEWORK = "소머즈"


def fetch() -> list[dict]:
    items = []
    for sub in REDDIT_SOCIAL:
        url = f"https://www.reddit.com/r/{sub}/new.json"
        res = base_fetch(url, params={"limit": 25})
        if not res:
            continue
        for post in res.json().get("data", {}).get("children", []):
            d = post.get("data", {})
            items.append({
                "name":        d.get("title", "")[:200],
                "description": (d.get("selftext", "") or "")[:300],
                "category":    "커뮤니티 반응",
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
