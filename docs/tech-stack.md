# 기술 스택

## Frontend / UI

**Streamlit**

선택 이유:
- 로컬 대시보드에 최적
- 가장 빠른 프로토타이핑
- 카드 UI 구현 용이
- Python과 완전 통합

```bash
streamlit run app.py
```

---

## Backend / 데이터 수집

**Python**

| 라이브러리 | 용도 |
|-----------|------|
| `requests` | HTTP 요청 |
| `BeautifulSoup4` | HTML 파싱 |
| `feedparser` | RSS/Atom 피드 수집 |
| `sqlite3` | DB 연동 (내장) |
| `Playwright` | 동적 사이트 (선택) |

---

## Database

**SQLite**

로컬 파일 기반, 별도 서버 불필요.

### 테이블 구조

```sql
-- 수집된 앱 정보
CREATE TABLE apps (
    id           INTEGER PRIMARY KEY,
    name         TEXT,
    description  TEXT,
    category     TEXT,
    source       TEXT,
    url          TEXT,
    collected_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 북마크
CREATE TABLE bookmarks (
    id       INTEGER PRIMARY KEY,
    app_id   INTEGER,
    memo     TEXT,
    tags     TEXT,
    saved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (app_id) REFERENCES apps(id)
);

-- 캘린더 메모 (하루 1개, 날짜별 기록)
CREATE TABLE daily_memos (
    id         INTEGER PRIMARY KEY,
    date       DATE UNIQUE,          -- YYYY-MM-DD
    content    TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);

-- 아이디어 컬렉션 (린 캔버스 9개 항목 포함)
CREATE TABLE ideas (
    id               INTEGER PRIMARY KEY,
    title            TEXT NOT NULL,
    description      TEXT,
    category         TEXT,
    tags             TEXT,               -- 쉼표 구분
    status           TEXT DEFAULT 'new', -- new / developing / done / hold
    source_date      DATE,               -- 어느 날 메모에서 나온 아이디어인지

    lc_customer_segments   TEXT,  -- 1. 고객 세그먼트
    lc_value_proposition   TEXT,  -- 2. 가치 제안
    lc_channels            TEXT,  -- 3. 채널
    lc_customer_relations  TEXT,  -- 4. 고객 관계
    lc_revenue_streams     TEXT,  -- 5. 수익원
    lc_key_resources       TEXT,  -- 6. 핵심 자원
    lc_key_activities      TEXT,  -- 7. 핵심 활동
    lc_key_partners        TEXT,  -- 8. 핵심 파트너
    lc_cost_structure      TEXT,  -- 9. 비용 구조

    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME
);

-- 태그
CREATE TABLE tags (
    id   INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);
```

---

## 프로젝트 구조

```
pm-insight-dashboard/
├── app.py                  # Streamlit 메인 앱 (페이지 라우팅)
├── README.md
│
├── crawler/
│   ├── base.py             # 공통 fetch / retry / User-Agent
│   │
│   ├── 주체찾기/
│   │   ├── producthunt.py
│   │   ├── hackernews.py
│   │   ├── appstore_rankings.py
│   │   └── indiehackers.py
│   │
│   ├── 시장쪼개기/
│   │   ├── appstore_categories.py
│   │   └── reddit_niche.py
│   │
│   ├── 소머즈/
│   │   ├── reddit_social.py
│   │   ├── naver_datalab.py
│   │   ├── google_trends.py
│   │   └── news_rss.py
│   │
│   └── 한끗차이/
│       ├── appstore_reviews.py
│       ├── googleplay_reviews.py
│       ├── producthunt_comments.py
│       └── reddit_wishlist.py
│
├── db/
│   └── database.db         # SQLite 파일
│
├── services/
│   ├── parser.py           # 수집 데이터 정제
│   ├── bookmark.py         # 북마크 CRUD
│   ├── memo.py             # 캘린더 메모 CRUD
│   └── idea.py             # 아이디어 CRUD
│
└── ui/
    ├── cards.py            # 앱 카드 컴포넌트
    ├── filters.py          # 필터/검색 UI
    ├── calendar.py         # 캘린더 메모 UI
    └── idea_browser.py     # 아이디어 카드 탐색 UI
```
