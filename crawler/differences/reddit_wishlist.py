from crawler.base import fetch as base_fetch

FRAMEWORK = "한끗차이"
SOURCE    = "Reddit"

QUERIES = [
    "wish there was an app",
    "why is there no app",
    "someone should make an app",
    "앱이 있으면 좋겠다",
    "이런 앱 없나",
    "app that does",
]


def fetch() -> list[dict]:
    items = []
    seen = set()
    for query in QUERIES:
        res = base_fetch(
            "https://www.reddit.com/search.json",
            params={"q": query, "sort": "new", "limit": 15, "type": "link"},
        )
        if not res:
            continue
        for post in res.json().get("data", {}).get("children", []):
            d = post.get("data", {})
            permalink = f"https://reddit.com{d.get('permalink','')}"
            if permalink in seen:
                continue
            seen.add(permalink)
            items.append({
                "name":        d.get("title", "")[:200],
                "description": (d.get("selftext", "") or "")[:300],
                "category":    "앱 개선 수요",
                "source":      f"Reddit (검색: {query})",
                "framework":   FRAMEWORK,
                "url":         permalink,
                "extra":       {
                    "score":    d.get("score", 0),
                    "query":    query,
                    "subreddit": d.get("subreddit", ""),
                },
            })
    return items
