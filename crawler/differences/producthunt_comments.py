import feedparser
from bs4 import BeautifulSoup
from crawler.base import fetch as base_fetch

FRAMEWORK = "한끗차이"
SOURCE    = "Product Hunt"
FEED_URL  = "https://www.producthunt.com/feed"


def fetch() -> list[dict]:
    feed = feedparser.parse(FEED_URL)
    items = []
    for entry in feed.entries[:10]:
        post_url = entry.get("link", "")
        if not post_url:
            continue
        res = base_fetch(post_url)
        if not res:
            continue
        soup = BeautifulSoup(res.text, "html.parser")
        # Product Hunt 댓글 셀렉터
        comment_els = soup.select("[data-test='comment-body']")
        for el in comment_els[:5]:
            text = el.get_text(strip=True)
            if len(text) < 30:
                continue
            items.append({
                "name":        f"[PH 댓글] {entry.get('title','')[:80]}",
                "description": text[:300],
                "category":    "사용자 반응",
                "source":      SOURCE,
                "framework":   FRAMEWORK,
                "url":         post_url,
                "extra":       {},
            })
    return items
