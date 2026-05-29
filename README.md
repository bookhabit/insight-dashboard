# 앱 기획 인사이트 대시보드

> 개인용 PM/기획 감각 훈련 시스템

매일 20~30분, 좋은 앱을 보고 → 저장하고 → 메모하고 → 아이디어를 꺼내보며 감각을 쌓는 로컬 대시보드.

---

## 빠른 시작 (처음 설치)

### 1. 클론

```bash
git clone https://github.com/bookhabit/insight-dashboard.git
cd insight-dashboard
```

### 2. 패키지 설치

```bash
python3 -m pip install -r requirements.txt
```

### 3. 환경변수 설정 (Naver DataLab 사용 시)

```bash
cp .env.example .env
```

`.env` 파일 열어서 키 입력:

```
NAVER_CLIENT_ID=발급받은_Client_ID
NAVER_CLIENT_SECRET=발급받은_Client_Secret
```

> Naver DataLab 키가 없어도 나머지 크롤러는 전부 정상 동작합니다.

### 4. 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 자동으로 열립니다.

---

## 화면 구성

```
┌──────────────────────────────────────────────┐
│  사이드바                                     │
│  ────────                                     │
│  📊 대시보드     수집된 앱 카드 목록           │
│  📅 캘린더 메모  날짜별 하루 기록              │
│  💡 아이디어     아이디어 서랍 + 린 캔버스     │
│  🔖 북마크       저장한 앱 모음               │
└──────────────────────────────────────────────┘
```

---

## 사용법

### 📊 대시보드

1. **`🔄 수집하기`** 버튼 클릭 → 14개 소스에서 자동 수집
2. 프레임워크 필터로 원하는 카테고리만 보기
   - `주체찾기` — Product Hunt, HN, App Store 랭킹
   - `시장쪼개기` — 카테고리별/국가별 앱 비교
   - `소머즈` — Reddit, 네이버 트렌드, 뉴스 RSS
   - `한끗차이` — 앱 1~2점 리뷰, 불만 수요
3. 마음에 드는 앱 **`🔖 북마크`** 저장

### 📅 캘린더 메모

1. 날짜 클릭 → 그날 메모 열기
2. 자유롭게 기록 (UX 관찰, 인사이트, 생각)
3. **`💾 저장`** — 해당 날짜에 저장 (다시 열면 그대로)
4. **`💡 아이디어로`** — 메모 내용을 아이디어 서랍으로 이동

> 메모가 있는 날은 달력에 `●` 점으로 표시됩니다.

### 💡 아이디어

**빠른 추가:**
- 상단 `➕ 아이디어 빠르게 추가` 열어서 제목만 써도 저장
- 캘린더에서 `💡 아이디어로` 버튼으로 자동 연결

**카드 탐색:**
- `← 이전` / `다음 →` 으로 한 장씩 탐색
- 하단 버튼으로 상태 변경
  - `💡 새 아이디어` → `🔨 발전 중` → `✅ 완성` / `🗑️ 보류`

**린 캔버스 디벨롭:**
- 카드에서 `🗂️ 린 캔버스 디벨롭 체크리스트` 열기
- 9개 항목을 천천히 채워가면 진행도 `▓▓▓░░░░░░ 3/9` 로 표시

| # | 항목 |
|---|------|
| 1 | 고객 세그먼트 |
| 2 | 가치 제안 |
| 3 | 채널 |
| 4 | 고객 관계 |
| 5 | 수익원 |
| 6 | 핵심 자원 |
| 7 | 핵심 활동 |
| 8 | 핵심 파트너 |
| 9 | 비용 구조 |

### 🔖 북마크

- 저장한 앱 목록 + 태그/메모 편집
- 태그로 필터링 (`#온보딩`, `#리텐션` 등)

---

## 수집 소스 (14개)

| 프레임워크 | 소스 |
|-----------|------|
| 주체찾기 | Product Hunt · Hacker News Show HN · App Store KR/US/JP · Indie Hackers |
| 시장쪼개기 | App Store 카테고리별×국가별 · Reddit 니치 커뮤니티 |
| 소머즈 | Reddit 소셜 · Naver DataLab · Google Trends · 뉴스 RSS 5개 |
| 한끗차이 | App Store 저평점 리뷰 · Google Play 저평점 리뷰 · PH 댓글 · Reddit 수요 검색 |

---

## 다른 컴퓨터에서 설치할 때

```bash
# 1. 클론
git clone https://github.com/bookhabit/insight-dashboard.git
cd insight-dashboard

# 2. 패키지
python3 -m pip install -r requirements.txt

# 3. 환경변수 (Naver 키 있을 경우)
cp .env.example .env
# .env 에 키 입력

# 4. 실행
streamlit run app.py
```

> `db/database.db` 는 gitignore 처리되어 있어 각 기기마다 독립적으로 쌓입니다.  
> `.env` 도 gitignore 처리되어 있어 키가 github에 올라가지 않습니다.

---

## 기술 스택

| 영역 | 도구 |
|------|------|
| UI | Streamlit |
| DB | SQLite (로컬 파일) |
| 크롤링 | requests · feedparser · BeautifulSoup · pytrends · google-play-scraper |
| 설정 | python-dotenv |

---

## 문서

| 문서 | 설명 |
|------|------|
| [docs/overview.md](docs/overview.md) | 프로젝트 목적 & 철학 |
| [docs/features.md](docs/features.md) | 기능 명세 |
| [docs/crawling-sources.md](docs/crawling-sources.md) | 크롤링 소스 전체 명세 |
| [docs/memo-calendar.md](docs/memo-calendar.md) | 캘린더 메모 설계 |
| [docs/idea-collection.md](docs/idea-collection.md) | 아이디어 컬렉션 설계 |
| [docs/tech-stack.md](docs/tech-stack.md) | 기술 스택 & DB 스키마 |
| [docs/roadmap.md](docs/roadmap.md) | 개발 로드맵 |
