from crawler.base import fetch as base_fetch

FRAMEWORK = "주체찾기"
SOURCE    = "Hacker News"
API_URL   = "https://hn.algolia.com/api/v1/search"


def fetch() -> list[dict]:
    res = base_fetch(API_URL, params={"tags": "show_hn", "hitsPerPage": 30})
    if not res:
        return []
    items = []
    for hit in res.json().get("hits", []):
        url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
        items.append({
            "name":        hit.get("title", ""),
            "description": "",
            "category":    "",
            "source":      SOURCE,
            "framework":   FRAMEWORK,
            "url":         url,
            "extra":       {
                "points":   hit.get("points", 0),
                "comments": hit.get("num_comments", 0),
            },
        })
    return items
