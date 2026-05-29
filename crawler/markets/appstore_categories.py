from crawler.base import fetch as base_fetch
from config import APPSTORE_CATEGORIES, APPSTORE_COUNTRIES

FRAMEWORK = "시장쪼개기"
SOURCE    = "App Store"


def fetch() -> list[dict]:
    items = []
    for country in APPSTORE_COUNTRIES:
        for cat_id, cat_name in APPSTORE_CATEGORIES.items():
            url = (
                f"https://rss.applemarketingtools.com/api/v2/{country}"
                f"/apps/top-free/50/{cat_id}/apps.json"
            )
            res = base_fetch(url)
            if not res:
                continue
            for entry in res.json().get("feed", {}).get("results", []):
                items.append({
                    "name":        entry.get("name", ""),
                    "description": entry.get("artistName", ""),
                    "category":    cat_name,
                    "source":      f"{SOURCE} {cat_name} ({country.upper()})",
                    "framework":   FRAMEWORK,
                    "url":         entry.get("url", ""),
                    "extra":       {
                        "app_id":   entry.get("id", ""),
                        "country":  country,
                        "category": cat_name,
                    },
                })
    return items
