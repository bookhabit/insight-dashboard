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


def _badge(text: str, color: str) -> str:
    return (
        f"<span style='background:{color};color:white;padding:2px 8px;"
        f"border-radius:10px;font-size:12px;'>{text}</span>"
    )


def render():
    st.title("📊 Dashboard")

    # 수집 버튼
    col_title, col_btn = st.columns([8, 2])
    with col_btn:
        if st.button("🔄 수집하기", use_container_width=True, type="primary"):
            _run_crawlers()

    st.divider()

    # 필터
    col1, col2, col3 = st.columns([3, 3, 4])
    with col1:
        fw_filter = st.selectbox("프레임워크", FRAMEWORK_OPTIONS, label_visibility="collapsed")
    with col2:
        search = st.text_input("검색", placeholder="🔍 키워드 검색", label_visibility="collapsed")
    with col3:
        sort_by = st.radio("정렬", ["최신순", "오래된순"], horizontal=True, label_visibility="collapsed")

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
