import streamlit as st
from services.bookmark import get_all_bookmarks, update_bookmark, remove_bookmark

FRAMEWORK_COLORS = {
    "주체찾기":  "#4A90D9",
    "시장쪼개기": "#7B68EE",
    "소머즈":    "#50C878",
    "한끗차이":  "#FF7043",
}


def render():
    st.title("🔖 북마크")

    bookmarks = get_all_bookmarks()
    if not bookmarks:
        st.info("아직 저장한 북마크가 없습니다.")
        return

    # 태그 필터
    all_tags = set()
    for bm in bookmarks:
        for t in (bm.get("tags") or "").replace(",", " ").split():
            t = t.strip().lstrip("#")
            if t:
                all_tags.add(t)

    tag_filter = ""
    if all_tags:
        tag_filter = st.selectbox(
            "태그 필터",
            ["전체"] + sorted(all_tags),
            label_visibility="collapsed",
        )

    search = st.text_input("검색", placeholder="🔍 이름/메모 검색", label_visibility="collapsed")

    # 필터 적용
    filtered = bookmarks
    if tag_filter and tag_filter != "전체":
        filtered = [b for b in filtered if tag_filter in (b.get("tags") or "")]
    if search:
        s = search.lower()
        filtered = [
            b for b in filtered
            if s in (b.get("name") or "").lower() or s in (b.get("memo") or "").lower()
        ]

    st.caption(f"총 {len(filtered)}개")
    st.divider()

    for bm in filtered:
        _render_bookmark_card(bm)


def _render_bookmark_card(bm: dict):
    fw    = bm.get("framework", "")
    color = FRAMEWORK_COLORS.get(fw, "#888")

    with st.container(border=True):
        c1, c2 = st.columns([9, 1])
        with c1:
            st.markdown(
                f"<span style='background:{color};color:white;padding:2px 8px;"
                f"border-radius:10px;font-size:11px;'>{fw}</span> "
                f"&nbsp;<small style='color:#888'>{bm.get('source','')}</small>",
                unsafe_allow_html=True,
            )
            st.markdown(f"**{bm['name'][:80]}**")
            if bm.get("url"):
                st.markdown(f"[🔗 링크 열기]({bm['url']})")
        with c2:
            if st.button("🗑", key=f"del_bm_{bm['id']}", help="북마크 삭제"):
                remove_bookmark(bm["app_id"] if "app_id" in bm else bm["id"])
                st.rerun()

        # 메모/태그 편집
        with st.expander("📝 메모 & 태그 편집"):
            new_memo = st.text_area(
                "메모",
                value=bm.get("memo") or "",
                height=80,
                key=f"bm_memo_{bm['id']}",
                label_visibility="collapsed",
                placeholder="이 앱에 대한 메모...",
            )
            new_tags = st.text_input(
                "태그",
                value=bm.get("tags") or "",
                key=f"bm_tags_{bm['id']}",
                label_visibility="collapsed",
                placeholder="#온보딩 #AI채팅 #리텐션",
            )
            if st.button("저장", key=f"bm_save_{bm['id']}"):
                update_bookmark(bm["id"], new_memo, new_tags)
                st.success("저장됐습니다.")
                st.rerun()
