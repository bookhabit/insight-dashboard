import streamlit as st
from db.schema import init_db

st.set_page_config(
    page_title="기획 인사이트 대시보드",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

PAGES = ["📊 대시보드", "📅 캘린더 메모", "💡 아이디어", "🔖 북마크"]

if "current_page" not in st.session_state:
    st.session_state.current_page = "📊 대시보드"

with st.sidebar:
    st.markdown("## 💡 기획 인사이트")
    st.divider()

    selected = st.radio(
        "메뉴",
        PAGES,
        index=PAGES.index(st.session_state.current_page),
        label_visibility="collapsed",
    )
    if selected != st.session_state.current_page:
        st.session_state.current_page = selected
        st.rerun()

    st.divider()
    st.caption("로컬 전용 · SQLite")

page = st.session_state.current_page

if page == "📊 대시보드":
    from ui.dashboard import render
    render()
elif page == "📅 캘린더 메모":
    from ui.calendar_view import render
    render()
elif page == "💡 아이디어":
    from ui.idea_browser import render
    render()
elif page == "🔖 북마크":
    from ui.bookmark_view import render
    render()
