from crawler.base import fetch as base_fetch
from config import APPSTORE_COUNTRIES

FRAMEWORK = "주체찾기"
SOURCE    = "App Store"


def fetch() -> list[dict]:
    items = []
    for country in APPSTORE_COUNTRIES:
        url = f"https://rss.applemarketingtools.com/api/v2/{country}/apps/top-free/100/apps.json"
        res = base_fetch(url)
        if not res:
            continue
        feed = res.json().get("feed", {})
        for entry in feed.get("results", []):
            items.append({
                "name":        entry.get("name", ""),
                "description": entry.get("artistName", ""),
                "category":    entry.get("genres", [{}])[0].get("name", "") if entry.get("genres") else "",
                "source":      f"{SOURCE} ({country.upper()})",
                "framework":   FRAMEWORK,
                "url":         entry.get("url", ""),
                "extra":       {
                    "app_id":      entry.get("id", ""),
                    "country":     country,
                    "artist_name": entry.get("artistName", ""),
                },
            })
    return items
