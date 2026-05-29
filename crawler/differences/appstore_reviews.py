from crawler.base import fetch as base_fetch
from config import APPSTORE_COUNTRIES

FRAMEWORK = "한끗차이"
SOURCE    = "App Store Reviews"


def _get_top_app_ids(country: str, limit: int = 20) -> list[str]:
    url = f"https://rss.applemarketingtools.com/api/v2/{country}/apps/top-free/{limit}/apps.json"
    res = base_fetch(url)
    if not res:
        return []
    return [r["id"] for r in res.json().get("feed", {}).get("results", [])]


def fetch() -> list[dict]:
    items = []
    for country in APPSTORE_COUNTRIES:
        app_ids = _get_top_app_ids(country, limit=10)
        for app_id in app_ids:
            url = (
                f"https://itunes.apple.com/{country}/rss/customerreviews"
                f"/page=1/id={app_id}/sortby=mostrecent/json"
            )
            res = base_fetch(url)
            if not res:
                continue
            feed = res.json().get("feed", {})
            app_name = ""
            for link in feed.get("link", []):
                if isinstance(link, dict) and link.get("attributes", {}).get("rel") == "alternate":
                    app_name = feed.get("title", {}).get("label", "")
                    break
            app_name = app_name or f"App {app_id}"

            for entry in feed.get("entry", []):
                if isinstance(entry, dict) and "im:rating" in entry:
                    rating = int(entry.get("im:rating", {}).get("label", "5"))
                    if rating <= 2:
                        title   = entry.get("title", {}).get("label", "")
                        content = entry.get("content", {}).get("label", "")
                        items.append({
                            "name":        f"[리뷰 {rating}★] {app_name}: {title}",
                            "description": content[:300],
                            "category":    "앱 리뷰",
                            "source":      f"{SOURCE} ({country.upper()})",
                            "framework":   FRAMEWORK,
                            "url":         f"https://apps.apple.com/{country}/app/id{app_id}",
                            "extra":       {
                                "app_id":  app_id,
                                "rating":  rating,
                                "country": country,
                            },
                        })
    return items
