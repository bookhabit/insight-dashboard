# 크롤링 소스 명세

## 프레임워크 구조

```
주체찾기       → 어떤 앱/서비스가 지금 나오고 있나
시장쪼개기     → 기존 시장을 더 잘게 나눠 새 기회 찾기
소머즈의 귀    → 사람들이 무엇을 말하고 있나 (소셜 + 트렌드 + 뉴스)
한 끗 차이     → 기존 서비스의 불만 → 개선 포인트 발굴
```

---

## 1. 주체찾기

### Product Hunt
> 매일 새로 런칭되는 앱의 핵심 피드

| 항목 | 내용 |
|------|------|
| 방법 | RSS |
| 엔드포인트 | `https://www.producthunt.com/feed` |
| 라이브러리 | `feedparser` |
| 수집 데이터 | 앱명, 한줄 설명, 투표수, URL, 태그 |
| 파일 | `crawler/주체찾기/producthunt.py` |

```python
import feedparser
feed = feedparser.parse("https://www.producthunt.com/feed")
```

---

### Hacker News — Show HN
> 만든 사람이 직접 올리는 프로덕트, 아이디어 원형 보기 최적

| 항목 | 내용 |
|------|------|
| 방법 | JSON API |
| 엔드포인트 | `https://hn.algolia.com/api/v1/search?tags=show_hn&hitsPerPage=30` |
| 라이브러리 | `requests` |
| 수집 데이터 | 제목, URL, 포인트, 댓글 수, 작성일 |
| 파일 | `crawler/주체찾기/hackernews.py` |

```python
import requests
res = requests.get("https://hn.algolia.com/api/v1/search", params={
    "tags": "show_hn", "hitsPerPage": 30
})
```

---

### App Store 카테고리별 랭킹 (한국/미국/일본)
> Apple 공식 RSS, 국가별 무료 앱 Top 100

| 항목 | 내용 |
|------|------|
| 방법 | JSON RSS |
| 엔드포인트 | `https://rss.applemarketingtools.com/api/v2/{country}/apps/top-free/{limit}/apps.json` |
| 국가 코드 | `kr` / `us` / `jp` |
| 라이브러리 | `requests` |
| 수집 데이터 | 앱명, 카테고리, 순위, 앱ID, URL |
| 파일 | `crawler/주체찾기/appstore_rankings.py` |

```python
countries = ["kr", "us", "jp"]
for country in countries:
    url = f"https://rss.applemarketingtools.com/api/v2/{country}/apps/top-free/100/apps.json"
```

---

### Indie Hackers
> 수익 공개하는 소규모 프로덕트 → 작은 시장 발굴

| 항목 | 내용 |
|------|------|
| 방법 | RSS |
| 엔드포인트 | `https://www.indiehackers.com/feed.rss` |
| 라이브러리 | `feedparser` |
| 수집 데이터 | 제목, 요약, URL, 작성일 |
| 파일 | `crawler/주체찾기/indiehackers.py` |

---

## 2. 시장쪼개기

### App Store 세부 카테고리 랭킹 (국가 비교)
> 같은 카테고리 내에서 한국만 뜨는 앱, 일본만 뜨는 앱 발견

| 항목 | 내용 |
|------|------|
| 방법 | JSON RSS |
| 엔드포인트 | `https://rss.applemarketingtools.com/api/v2/{country}/apps/top-free/100/{category_id}/apps.json` |
| 라이브러리 | `requests` |
| 파일 | `crawler/시장쪼개기/appstore_categories.py` |

**주요 카테고리 ID:**

| ID | 카테고리 |
|----|----------|
| `6000` | Business |
| `6007` | Productivity |
| `6013` | Health & Fitness |
| `6017` | Education |
| `6018` | Finance |
| `6020` | Social Networking |
| `6023` | Food & Drink |

```python
categories = {"6007": "Productivity", "6013": "Health", "6020": "Social"}
countries  = ["kr", "us", "jp"]
# 조합별 랭킹 수집 → 국가 간 차이 비교
```

---

### Reddit 니치 커뮤니티
> 좁은 타겟의 실제 수요 확인

| 항목 | 내용 |
|------|------|
| 방법 | JSON API (인증 불필요) |
| 엔드포인트 | `https://www.reddit.com/r/{subreddit}/hot.json?limit=25` |
| 라이브러리 | `requests` |
| 파일 | `crawler/시장쪼개기/reddit_niche.py` |

**수집 대상 서브레딧:**

| 서브레딧 | 목적 |
|----------|------|
| `r/productivity` | 생산성 앱 수요 |
| `r/sleep` | 수면 앱 틈새 |
| `r/ADHD` | ADHD 관련 도구 |
| `r/financialindependence` | 재정 앱 수요 |
| `r/loseit` | 다이어트/헬스 앱 |
| `r/selfimprovement` | 루틴/성장 앱 |
| `r/digitalnomad` | 리모트/워크툴 |

---

## 3. 소머즈의 귀

### Reddit — 소셜 모니터링
> 사람들의 솔직한 반응, 페인포인트, 칭찬 텍스트

| 항목 | 내용 |
|------|------|
| 방법 | JSON API |
| 엔드포인트 | `https://www.reddit.com/r/{subreddit}/new.json?limit=25` |
| 라이브러리 | `requests` |
| 파일 | `crawler/소머즈/reddit_social.py` |

**수집 대상 서브레딧:**

| 서브레딧 | 목적 |
|----------|------|
| `r/apps` | 앱 전반 반응 |
| `r/startups` | 스타트업 트렌드 |
| `r/SideProject` | 개인 프로젝트 |
| `r/AppIdeas` | 앱 아이디어 공유 |
| `r/entrepreneur` | 창업 관련 |

---

### Naver DataLab
> 한국 시장 검색 트렌드 추적 (공식 API)

| 항목 | 내용 |
|------|------|
| 방법 | REST API |
| 엔드포인트 | `https://openapi.naver.com/v1/datalab/search` |
| 인증 | 네이버 개발자센터 API 키 필요 (무료) |
| 라이브러리 | `requests` |
| 파일 | `crawler/소머즈/naver_datalab.py` |

```python
headers = {
    "X-Naver-Client-Id": CLIENT_ID,
    "X-Naver-Client-Secret": CLIENT_SECRET,
    "Content-Type": "application/json"
}
body = {
    "startDate": "2026-01-01",
    "endDate": "2026-05-29",
    "timeUnit": "week",
    "keywordGroups": [{"groupName": "루틴앱", "keywords": ["루틴", "습관"]}]
}
```

---

### Google Trends
> 글로벌 관심사 변화 추적

| 항목 | 내용 |
|------|------|
| 방법 | 비공식 API 래퍼 |
| 라이브러리 | `pytrends` |
| 파일 | `crawler/소머즈/google_trends.py` |

```python
from pytrends.request import TrendReq
pt = TrendReq(hl="ko-KR", tz=540)
pt.build_payload(["루틴 앱", "감정 기록"], timeframe="today 3-m", geo="KR")
df = pt.interest_over_time()
```

---

### 업계 뉴스 RSS
> 업계 흐름 구독

| 소스 | RSS URL | 파일 |
|------|---------|------|
| 요즘IT | `https://yozm.wishket.com/magazine/rss/` | `crawler/소머즈/news_rss.py` |
| Platum | `https://platum.kr/feed` | 동일 |
| TechCrunch | `https://techcrunch.com/feed/` | 동일 |
| The Verge | `https://www.theverge.com/rss/index.xml` | 동일 |
| Fast Company | `https://www.fastcompany.com/latest/rss` | 동일 |

```python
NEWS_FEEDS = [
    {"name": "요즘IT",      "url": "https://yozm.wishket.com/magazine/rss/"},
    {"name": "Platum",      "url": "https://platum.kr/feed"},
    {"name": "TechCrunch",  "url": "https://techcrunch.com/feed/"},
    {"name": "The Verge",   "url": "https://www.theverge.com/rss/index.xml"},
    {"name": "Fast Company","url": "https://www.fastcompany.com/latest/rss"},
]
```

---

## 4. 한 끗 차이 만들기

### App Store 리뷰 (1~2점)
> 기존 앱의 불만 직접 수집

| 항목 | 내용 |
|------|------|
| 방법 | iTunes RSS |
| 엔드포인트 | `https://itunes.apple.com/{country}/rss/customerreviews/page=1/id={app_id}/sortby=mostrecent/json` |
| 흐름 | App Store 랭킹으로 앱ID 수집 → 각 앱의 리뷰 수집 |
| 라이브러리 | `requests` |
| 파일 | `crawler/한끗차이/appstore_reviews.py` |

```python
# 랭킹에서 수집한 app_id 활용
def fetch_reviews(app_id: str, country: str = "kr"):
    url = f"https://itunes.apple.com/{country}/rss/customerreviews/page=1/id={app_id}/sortby=mostrecent/json"
    # rating 1~2점만 필터링
```

---

### Google Play 리뷰 (1~2점)
> 안드로이드 사용자 불만 수집

| 항목 | 내용 |
|------|------|
| 방법 | 스크래핑 라이브러리 |
| 라이브러리 | `google-play-scraper` |
| 파일 | `crawler/한끗차이/googleplay_reviews.py` |

```python
from google_play_scraper import reviews, Sort

result, _ = reviews(
    "com.example.app",
    lang="ko",
    country="kr",
    sort=Sort.NEWEST,
    count=100,
    filter_score_with=2  # 1~2점 필터
)
```

---

### Product Hunt 댓글
> "이 기능이 있었으면", "이게 아쉽다" 패턴

| 항목 | 내용 |
|------|------|
| 방법 | BeautifulSoup 스크래핑 |
| 라이브러리 | `requests` + `bs4` |
| 파일 | `crawler/한끗차이/producthunt_comments.py` |

---

### Reddit — 앱 개선 수요
> "이런 앱 없나요?" 실제 수요 발굴

| 항목 | 내용 |
|------|------|
| 방법 | Reddit Search JSON API |
| 엔드포인트 | `https://www.reddit.com/search.json?q={query}&sort=new&limit=25` |
| 라이브러리 | `requests` |
| 파일 | `crawler/한끗차이/reddit_wishlist.py` |

```python
queries = [
    "wish there was an app",
    "why is there no app",
    "someone should make an app",
    "앱이 있으면 좋겠다",
    "이런 앱 없나",
]
```

---

## 크롤러 파일 구조

```
crawler/
├── base.py                        # 공통 fetch / retry / User-Agent 설정
│
├── 주체찾기/
│   ├── producthunt.py
│   ├── hackernews.py
│   ├── appstore_rankings.py
│   └── indiehackers.py
│
├── 시장쪼개기/
│   ├── appstore_categories.py
│   └── reddit_niche.py
│
├── 소머즈/
│   ├── reddit_social.py
│   ├── naver_datalab.py
│   ├── google_trends.py
│   └── news_rss.py
│
└── 한끗차이/
    ├── appstore_reviews.py
    ├── googleplay_reviews.py
    ├── producthunt_comments.py
    └── reddit_wishlist.py
```

---

## 수집 방법 요약

| 방법 | 소스 수 | 라이브러리 |
|------|---------|-----------|
| RSS (feedparser) | Product Hunt, Indie Hackers, 뉴스 5개 | `feedparser` |
| JSON API | Hacker News, App Store, Reddit (전체), Naver DataLab | `requests` |
| 비공식 API 래퍼 | Google Trends | `pytrends` |
| 스크래핑 라이브러리 | Google Play 리뷰 | `google-play-scraper` |
| BeautifulSoup | Product Hunt 댓글 | `requests` + `bs4` |

```bash
pip install feedparser requests pytrends google-play-scraper beautifulsoup4
```
