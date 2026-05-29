# 데이터 흐름

## 전체 흐름

```
크롤링 (crawler/)
    ↓
데이터 정제 (services/parser.py)
    ↓
SQLite 저장 (db/database.db)
    ↓
Streamlit 출력 (app.py + ui/)
    ↓
북마크 / 메모 (services/bookmark.py)
```

---

## 수집 소스별 방식

| 소스 | 방식 | 비고 |
|------|------|------|
| Product Hunt | RSS 피드 / API | `feedparser` 활용 |
| Reddit | JSON API | 공개 API (`/r/xxx.json`) |
| App Store | 랭킹 RSS | Apple 공식 RSS 제공 |
| GitHub Trending | HTML 파싱 | `BeautifulSoup` |
| Mobbin / Dribbble | 수동 저장 | 크롤링 어려움, 직접 입력 |

---

## 크롤링 주기

### 방법 1 — 앱 실행 시 수집 (기본)
```python
# app.py 실행 시 자동으로 최신 데이터 수집
if is_stale(last_updated, hours=6):
    run_crawlers()
```

### 방법 2 — 스케줄러 (선택)
```python
import schedule

schedule.every().day.at("07:00").do(run_crawlers)
```

매일 오전 7시 자동 수집. 앱과 별도로 백그라운드 실행.

---

## 데이터 정제 규칙

`services/parser.py` 처리 항목:

- 중복 URL 제거
- 설명 텍스트 길이 제한 (200자)
- 카테고리 자동 분류 (키워드 기반)
- 수집 시각 타임스탬프 기록
