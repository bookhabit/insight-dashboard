import time
import logging
import requests

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def fetch(url: str, params: dict = None, headers: dict = None, retries: int = 3) -> requests.Response | None:
    h = {**HEADERS, **(headers or {})}
    for attempt in range(retries):
        try:
            res = requests.get(url, params=params, headers=h, timeout=15)
            res.raise_for_status()
            return res
        except Exception as e:
            logger.warning(f"[{attempt+1}/{retries}] {url} — {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    return None
