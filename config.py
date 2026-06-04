import os
from dotenv import load_dotenv

load_dotenv()

NAVER_CLIENT_ID     = os.getenv("NAVER_CLIENT_ID", "")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "")

TREND_KEYWORDS_KR = ["루틴 앱", "감정 기록", "생산성 앱", "AI 챗봇", "습관 트래커"]
TREND_KEYWORDS_EN = ["routine app", "productivity app", "AI assistant", "habit tracker"]

REDDIT_SOCIAL = ["apps", "startups", "SideProject", "AppIdeas", "entrepreneur"]
REDDIT_NICHE  = ["productivity", "sleep", "ADHD", "financialindependence", "loseit", "selfimprovement", "digitalnomad"]

APPSTORE_CATEGORIES = {
    "6007": "Productivity",
    "6013": "Health & Fitness",
    "6020": "Social Networking",
    "6000": "Business",
    "6017": "Education",
}
APPSTORE_COUNTRIES = ["kr", "us", "jp"]

GOOGLE_PLAY_APP_IDS = [
    "com.todoist.prod.Todoist",
    "com.notion.id",
    "com.duolingo",
    "com.daylio.journal",
    "com.fabulous.android",
    "com.calm.android",
    "com.robinhood.android",
]

NEWS_FEEDS = [
    {"name": "요즘IT",       "url": "https://yozm.wishket.com/magazine/rss/",      "framework": "소머즈"},
    {"name": "Platum",       "url": "https://platum.kr/feed",                      "framework": "소머즈"},
    {"name": "TechCrunch Apps",     "url": "https://techcrunch.com/category/apps/feed/",     "framework": "소머즈"},
    {"name": "TechCrunch Security", "url": "https://techcrunch.com/category/security/feed/", "framework": "소머즈"},
    {"name": "The Verge",    "url": "https://www.theverge.com/rss/index.xml",      "framework": "소머즈"},
    {"name": "Fast Company", "url": "https://www.fastcompany.com/latest/rss",      "framework": "소머즈"},
]
