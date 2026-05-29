import json
import logging
import requests
from datetime import date, timedelta
from config import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET, TREND_KEYWORDS_KR

FRAMEWORK = "소머즈"
API_URL   = "https://openapi.naver.com/v1/datalab/search"
logger    = logging.getLogger(__name__)


def fetch() -> list[dict]:
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        logger.info("Naver DataLab: API 키 없음, 건너뜀")
        return []

    end   = date.today()
    start = end - timedelta(days=30)
    keyword_groups = [{"groupName": kw, "keywords": [kw]} for kw in TREND_KEYWORDS_KR]

    body = {
        "startDate":     start.strftime("%Y-%m-%d"),
        "endDate":       end.strftime("%Y-%m-%d"),
        "timeUnit":      "week",
        "keywordGroups": keyword_groups,
    }
    headers = {
        "X-Naver-Client-Id":     NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
        "Content-Type":          "application/json",
    }

    try:
        res = requests.post(API_URL, headers=headers, data=json.dumps(body), timeout=15)
    except requests.exceptions.RequestException as e:
        logger.warning(f"Naver DataLab 요청 실패: {e}")
        return []

    # 일일 한도 초과 (429) 또는 기타 오류
    if res.status_code == 429:
        logger.warning("Naver DataLab: 일일 호출 한도 초과 (1,000회/일). 내일 다시 수집됩니다.")
        return []
    if res.status_code == 401:
        logger.warning("Naver DataLab: API 키 인증 실패. .env를 확인하세요.")
        return []
    if not res.ok:
        logger.warning(f"Naver DataLab: 응답 오류 {res.status_code} — {res.text[:200]}")
        return []

    data = res.json()
    if "errorMessage" in data:
        logger.warning(f"Naver DataLab API 오류: {data['errorMessage']}")
        return []

    items = []
    for result in data.get("results", []):
        title   = result.get("title", "")
        periods = result.get("data", [])
        if not periods:
            continue
        latest = periods[-1]
        items.append({
            "name":        f"[네이버 트렌드] {title}",
            "description": f"최근 검색 관심도: {latest.get('ratio', 0):.1f} (기간: {start} ~ {end})",
            "category":    "트렌드",
            "source":      "Naver DataLab",
            "framework":   FRAMEWORK,
            "url":         "https://datalab.naver.com/keyword/trendSearch.naver",
            "extra":       {"keyword": title, "data": periods},
        })
    return items
