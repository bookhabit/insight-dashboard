import streamlit as st
from db.schema import get_conn
from services.bookmark import add_bookmark, is_bookmarked

FRAMEWORK_COLORS = {
    "주체찾기":  "#4A90D9",
    "시장쪼개기": "#7B68EE",
    "소머즈":    "#50C878",
    "한끗차이":  "#FF7043",
}

FRAMEWORK_OPTIONS = ["전체", "주체찾기", "시장쪼개기", "소머즈", "한끗차이"]

FRAMEWORK_GUIDE = {
    "주체찾기": {
        "subtitle": "어떤 앱/서비스가 지금 나오고 있나",
        "mindset": "🎯 읽는 마인드셋",
        "description": (
            "지금 이 시점에 **누가** 무엇을 만들어 **세상에 내놓고 있는가**를 보는 시각입니다. "
            "좋은 앱인지 판단하기 전에, 먼저 **어떤 문제를 잡았는가**를 파악하세요."
        ),
        "questions": [
            "이 앱은 어떤 불편함을 해결하려 했나?",
            "지금 이 시점에 왜 이 앱이 나왔을까? (트리거가 뭔가)",
            "타겟 사용자는 어떤 사람인가?",
            "한 줄로 요약하면 어떤 앱인가?",
        ],
        "tip": "💡 Product Hunt·App Store 1위 앱의 공통 패턴을 찾으면 트렌드가 보입니다.",
        "sources": "Product Hunt · Hacker News Show HN · App Store KR/US/JP 랭킹 · Indie Hackers",
    },
    "시장쪼개기": {
        "subtitle": "기존 시장을 더 잘게 나눠 새 기회 찾기",
        "mindset": "🔬 읽는 마인드셋",
        "description": (
            "큰 시장(생산성, 헬스, 교육) 안에서 **아직 덜 된 틈새**를 찾는 시각입니다. "
            "같은 카테고리라도 **한국·미국·일본**에서 다르게 반응하는 앱이 있다면, "
            "그 이유를 추적하는 게 핵심입니다."
        ),
        "questions": [
            "이 앱은 어떤 더 큰 시장의 '조각'인가?",
            "한국에서 뜨는데 미국엔 없는 이유가 뭔가? (또는 반대)",
            "같은 카테고리 앱들과 뭐가 다른가?",
            "이 니치(niche) 사용자는 기존 서비스 어디서 불편함을 겪었나?",
        ],
        "tip": "💡 r/ADHD, r/loseit 같은 서브레딧은 특정 집단의 원초적인 욕구가 드러나는 공간입니다.",
        "sources": "App Store 카테고리별×국가별 · Reddit 니치 커뮤니티",
    },
    "소머즈": {
        "subtitle": "사람들이 무엇을 말하고 있나",
        "mindset": "👂 읽는 마인드셋",
        "description": (
            "직접 만들기 전에 **사람들의 언어로 세상을 듣는** 단계입니다. "
            "트렌드 키워드가 오르는 게 보이면 **왜 지금인가**를 생각하고, "
            "뉴스·커뮤니티 글에서 반복되는 주제를 찾으세요."
        ),
        "questions": [
            "요즘 사람들이 가장 많이 검색/이야기하는 게 뭔가?",
            "이 트렌드가 3개월 후에도 유효할까, 아니면 일시적인가?",
            "이 주제로 앱을 만든다면 어떤 기능이 핵심일까?",
            "한국 트렌드와 글로벌 트렌드 사이에 갭이 있는가?",
        ],
        "tip": "💡 Naver DataLab 키워드가 급상승한다면, 그 수요를 채우는 앱이 아직 없을 가능성이 있습니다.",
        "sources": "Reddit 소셜 · Naver DataLab · Google Trends · 요즘IT·Platum·TechCrunch·The Verge·Fast Company",
    },
    "한끗차이": {
        "subtitle": "기존 서비스의 불만 → 개선 포인트 발굴",
        "mindset": "🩺 읽는 마인드셋",
        "description": (
            "별점 1~2점 리뷰와 '이런 앱 없나요?' 게시글은 **아직 해결 안 된 진짜 수요**입니다. "
            "불만 글을 읽을 때 '이 사람이 원한 게 뭔가'를 역으로 추적하세요. "
            "거기서 한 끗 나은 서비스 아이디어가 나옵니다."
        ),
        "questions": [
            "이 불만의 본질적인 원인이 뭔가? (기능 문제 vs 설계 문제 vs 기대치 문제)",
            "같은 불만이 여러 앱에서 반복된다면, 업계 전체의 맹점 아닐까?",
            "'이런 앱 없나요?' 글에서 가장 많이 등장하는 키워드는?",
            "내가 이 불만을 해결한다면, MVP로 뭘 만들면 충분할까?",
        ],
        "tip": "💡 별점 1점 리뷰에서 진짜 페인포인트를 찾고, Reddit Wishlist에서 수요를 교차 검증하세요.",
        "sources": "App Store 저평점 리뷰 · Google Play 저평점 리뷰 · Product Hunt 댓글 · Reddit 수요 검색",
    },
}


def _badge(text: str, color: str) -> str:
    return (
        f"<span style='background:{color};color:white;padding:2px 8px;"
        f"border-radius:10px;font-size:12px;'>{text}</span>"
    )


def render():
    st.title("📊 앱 인사이트 대시보드")

    # 수집 버튼
    col_title, col_btn = st.columns([8, 2])
    with col_btn:
        if st.button("🔄 수집하기", use_container_width=True, type="primary"):
            _run_crawlers()

    st.divider()

    # 프레임워크 버튼 필터
    if "fw_filter" not in st.session_state:
        st.session_state.fw_filter = "전체"

    btn_cols = st.columns(5)
    btn_labels = ["전체", "주체찾기", "시장쪼개기", "소머즈", "한끗차이"]
    for i, label in enumerate(btn_labels):
        with btn_cols[i]:
            is_active = st.session_state.fw_filter == label
            if st.button(
                label,
                key=f"fw_btn_{label}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.fw_filter = label
                st.rerun()

    fw_filter = st.session_state.fw_filter

    # 검색 + 정렬
    col2, col3 = st.columns([6, 4])
    with col2:
        search = st.text_input("검색", placeholder="🔍 키워드 검색", label_visibility="collapsed")
    with col3:
        sort_by = st.radio("정렬", ["최신순", "오래된순"], horizontal=True, label_visibility="collapsed")

    # 프레임워크 읽기 가이드
    if fw_filter != "전체" and fw_filter in FRAMEWORK_GUIDE:
        _render_framework_guide(fw_filter)

    # 데이터 조회
    conn   = get_conn()
    query  = "SELECT * FROM apps"
    params = []
    where  = []
    if fw_filter != "전체":
        where.append("framework = ?")
        params.append(fw_filter)
    if search:
        where.append("(name LIKE ? OR description LIKE ?)")
        params += [f"%{search}%", f"%{search}%"]
    if where:
        query += " WHERE " + " AND ".join(where)
    query += " ORDER BY collected_at " + ("DESC" if sort_by == "최신순" else "ASC")
    query += " LIMIT 60"

    apps = [dict(r) for r in conn.execute(query, params).fetchall()]
    conn.close()

    if not apps:
        st.info("수집된 앱이 없습니다. '수집하기' 버튼을 눌러 데이터를 가져오세요.")
        return

    st.caption(f"총 {len(apps)}개")

    cols = st.columns(3)
    for i, app in enumerate(apps):
        with cols[i % 3]:
            _render_card(app)


def _render_framework_guide(fw: str):
    g     = FRAMEWORK_GUIDE[fw]
    color = FRAMEWORK_COLORS.get(fw, "#888")

    with st.expander(f"{g['mindset']} — {fw}: {g['subtitle']}", expanded=False):
        st.markdown(g["description"])

        st.markdown("**이런 질문을 갖고 읽어보세요:**")
        for q in g["questions"]:
            st.markdown(f"- {q}")

        st.markdown(
            f"<div style='margin-top:10px;padding:8px 12px;background:#f8f9fa;"
            f"border-left:3px solid {color};border-radius:4px;font-size:13px'>"
            f"{g['tip']}</div>",
            unsafe_allow_html=True,
        )

        st.caption(f"📡 수집 소스: {g['sources']}")


def _render_card(app: dict):
    fw    = app.get("framework", "")
    color = FRAMEWORK_COLORS.get(fw, "#888")

    with st.container(border=True):
        st.markdown(
            f"{_badge(fw, color)} &nbsp; <small style='color:#888'>{app.get('source','')}</small>",
            unsafe_allow_html=True,
        )
        st.markdown(f"**{app['name'][:60]}**")
        if app.get("description"):
            st.caption(app["description"][:120])

        c1, c2 = st.columns([5, 5])
        with c1:
            if app.get("url"):
                st.markdown(f"[🔗 링크]({app['url']})")
        with c2:
            already = is_bookmarked(app["id"])
            label   = "✅ 저장됨" if already else "🔖 북마크"
            if st.button(label, key=f"bm_{app['id']}", use_container_width=True,
                         disabled=already):
                add_bookmark(app["id"])
                st.rerun()


def _run_crawlers():
    from crawler.runner import run_all

    progress_bar = st.progress(0, text="수집 준비 중...")

    def cb(pct, msg):
        progress_bar.progress(pct, text=msg)

    saved, errors = run_all(progress_callback=cb)
    progress_bar.empty()

    if errors:
        with st.expander(f"⚠️ {len(errors)}개 크롤러 실패"):
            for e in errors:
                st.text(e)

    st.success(f"✅ 새 항목 {saved}개 저장 완료")
    st.rerun()
