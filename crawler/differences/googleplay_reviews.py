from config import GOOGLE_PLAY_APP_IDS

FRAMEWORK = "한끗차이"
SOURCE    = "Google Play Reviews"


def fetch() -> list[dict]:
    try:
        from google_play_scraper import app as gp_app, reviews, Sort
    except ImportError:
        return []

    items = []
    for app_id in GOOGLE_PLAY_APP_IDS:
        try:
            info = gp_app(app_id, lang="ko", country="kr")
            app_name = info.get("title", app_id)
        except Exception:
            app_name = app_id

        for lang, country in [("ko", "kr"), ("en", "us")]:
            try:
                result, _ = reviews(
                    app_id,
                    lang=lang,
                    country=country,
                    sort=Sort.NEWEST,
                    count=30,
                )
            except Exception:
                continue
            for r in result:
                if r.get("score", 5) <= 2:
                    items.append({
                        "name":        f"[리뷰 {r['score']}★] {app_name}: {r.get('userName','')}",
                        "description": r.get("content", "")[:300],
                        "category":    "앱 리뷰",
                        "source":      f"{SOURCE} ({country.upper()})",
                        "framework":   FRAMEWORK,
                        "url":         f"https://play.google.com/store/apps/details?id={app_id}",
                        "extra":       {
                            "app_id":  app_id,
                            "rating":  r.get("score"),
                            "country": country,
                        },
                    })
    return items
