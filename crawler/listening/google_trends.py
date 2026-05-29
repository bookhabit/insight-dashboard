from config import TREND_KEYWORDS_KR, TREND_KEYWORDS_EN

FRAMEWORK = "소머즈"


def fetch() -> list[dict]:
    try:
        from pytrends.request import TrendReq
    except ImportError:
        return []

    items = []

    # 한국 트렌드
    try:
        pt = TrendReq(hl="ko-KR", tz=540)
        pt.build_payload(TREND_KEYWORDS_KR[:5], timeframe="today 3-m", geo="KR")
        df = pt.interest_over_time()
        if not df.empty:
            for kw in TREND_KEYWORDS_KR[:5]:
                if kw in df.columns:
                    avg = df[kw].mean()
                    items.append({
                        "name":        f"[Google 트렌드 KR] {kw}",
                        "description": f"최근 3개월 평균 관심도: {avg:.1f}",
                        "category":    "트렌드",
                        "source":      "Google Trends (KR)",
                        "framework":   FRAMEWORK,
                        "url":         f"https://trends.google.com/trends/explore?q={kw}&geo=KR",
                        "extra":       {"keyword": kw, "avg_interest": round(avg, 1)},
                    })
    except Exception:
        pass

    # 글로벌 트렌드
    try:
        pt = TrendReq(hl="en-US", tz=0)
        pt.build_payload(TREND_KEYWORDS_EN[:5], timeframe="today 3-m")
        df = pt.interest_over_time()
        if not df.empty:
            for kw in TREND_KEYWORDS_EN[:5]:
                if kw in df.columns:
                    avg = df[kw].mean()
                    items.append({
                        "name":        f"[Google Trends Global] {kw}",
                        "description": f"3-month avg interest: {avg:.1f}",
                        "category":    "트렌드",
                        "source":      "Google Trends (Global)",
                        "framework":   FRAMEWORK,
                        "url":         f"https://trends.google.com/trends/explore?q={kw}",
                        "extra":       {"keyword": kw, "avg_interest": round(avg, 1)},
                    })
    except Exception:
        pass

    return items
