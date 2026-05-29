import logging
from typing import Callable

logger = logging.getLogger(__name__)

_CRAWLERS: list[tuple[str, Callable]] = [
    # 주체찾기
    ("Product Hunt",            "crawler.subjects.producthunt",             "fetch"),
    ("Hacker News Show HN",     "crawler.subjects.hackernews",              "fetch"),
    ("App Store Rankings",      "crawler.subjects.appstore_rankings",       "fetch"),
    ("Indie Hackers",           "crawler.subjects.indiehackers",            "fetch"),
    # 시장쪼개기
    ("App Store Categories",    "crawler.markets.appstore_categories",      "fetch"),
    ("Reddit Niche",            "crawler.markets.reddit_niche",             "fetch"),
    # 소머즈의 귀
    ("Reddit Social",           "crawler.listening.reddit_social",          "fetch"),
    ("Naver DataLab",           "crawler.listening.naver_datalab",          "fetch"),
    ("Google Trends",           "crawler.listening.google_trends",          "fetch"),
    ("News RSS",                "crawler.listening.news_rss",               "fetch"),
    # 한 끗 차이
    ("App Store Reviews",       "crawler.differences.appstore_reviews",     "fetch"),
    ("Google Play Reviews",     "crawler.differences.googleplay_reviews",   "fetch"),
    ("Product Hunt Comments",   "crawler.differences.producthunt_comments", "fetch"),
    ("Reddit Wishlist",         "crawler.differences.reddit_wishlist",      "fetch"),
]


def run_all(progress_callback=None) -> tuple[int, list[str]]:
    from services.parser import save_items

    all_items = []
    errors    = []
    total     = len(_CRAWLERS)

    for i, (name, module_path, fn_name) in enumerate(_CRAWLERS):
        if progress_callback:
            progress_callback(i / total, f"{name} 수집 중...")
        try:
            import importlib
            mod   = importlib.import_module(module_path)
            items = getattr(mod, fn_name)()
            all_items.extend(items)
            logger.info(f"[{name}] {len(items)}개 수집")
        except Exception as e:
            msg = f"{name}: {e}"
            errors.append(msg)
            logger.warning(f"크롤러 실패 — {msg}")

    if progress_callback:
        progress_callback(1.0, "저장 중...")

    saved = save_items(all_items)

    if progress_callback:
        progress_callback(1.0, "완료")

    return saved, errors
