import calendar
import streamlit as st
from datetime import date
from services.memo import get_memo, save_memo, get_memo_dates


def render():
    st.title("📅 캘린더 메모")

    _init_state()

    year  = st.session_state.cal_year
    month = st.session_state.cal_month

    # 월 네비게이션
    c1, c2, c3 = st.columns([1, 5, 1])
    with c1:
        if st.button("◀", use_container_width=True):
            _prev_month()
            st.rerun()
    with c2:
        st.markdown(
            f"<h3 style='text-align:center;margin:0'>{year}년 {month}월</h3>",
            unsafe_allow_html=True,
        )
    with c3:
        if st.button("▶", use_container_width=True):
            _next_month()
            st.rerun()

    st.write("")

    # 메모 있는 날짜 목록
    memo_dates = get_memo_dates(year, month)
    today      = str(date.today())

    # 요일 헤더
    day_headers = ["월", "화", "수", "목", "금", "토", "일"]
    header_cols = st.columns(7)
    for i, h in enumerate(day_headers):
        header_cols[i].markdown(
            f"<div style='text-align:center;font-weight:600;color:#888;padding:4px'>{h}</div>",
            unsafe_allow_html=True,
        )

    # 달력 그리드
    month_weeks = calendar.monthcalendar(year, month)
    for week in month_weeks:
        week_cols = st.columns(7)
        for col_idx, day in enumerate(week):
            with week_cols[col_idx]:
                if day == 0:
                    st.write("")
                    continue
                date_str = f"{year:04d}-{month:02d}-{day:02d}"
                has_memo = date_str in memo_dates
                is_today = date_str == today
                is_sel   = date_str == st.session_state.selected_date

                dot   = "●" if has_memo else " "
                style = "primary" if is_sel else "secondary"

                label = f"**{day}**\n{dot}" if is_today else f"{day}\n{dot}"
                if st.button(label, key=f"cal_{date_str}", use_container_width=True, type=style):
                    st.session_state.selected_date = date_str
                    st.rerun()

    st.divider()

    # 메모 에디터
    selected = st.session_state.selected_date
    sel_date = date.fromisoformat(selected)
    weekday  = ["월", "화", "수", "목", "금", "토", "일"][sel_date.weekday()]
    st.subheader(f"📝 {sel_date.year}년 {sel_date.month}월 {sel_date.day}일 ({weekday})")

    existing = get_memo(selected)
    content  = st.text_area(
        "메모",
        value=existing,
        height=220,
        placeholder="오늘 본 앱, UX 패턴, 인상적인 흐름, 떠오른 생각을 자유롭게 기록하세요...",
        key=f"memo_input_{selected}",
        label_visibility="collapsed",
    )

    c_save, c_promote = st.columns([8, 2])
    with c_save:
        if st.button("💾 저장", key=f"save_{selected}", use_container_width=True):
            save_memo(selected, content)
            st.success("저장됐습니다.")
            st.rerun()
    with c_promote:
        if st.button("💡 아이디어로", key=f"promote_{selected}", use_container_width=True):
            st.session_state["promote_content"] = content
            st.session_state["promote_date"]    = selected
            st.session_state["current_page"]    = "💡 아이디어"
            st.rerun()


def _init_state():
    today = date.today()
    if "cal_year"       not in st.session_state:
        st.session_state.cal_year      = today.year
    if "cal_month"      not in st.session_state:
        st.session_state.cal_month     = today.month
    if "selected_date"  not in st.session_state:
        st.session_state.selected_date = str(today)


def _prev_month():
    if st.session_state.cal_month == 1:
        st.session_state.cal_month = 12
        st.session_state.cal_year -= 1
    else:
        st.session_state.cal_month -= 1


def _next_month():
    if st.session_state.cal_month == 12:
        st.session_state.cal_month = 1
        st.session_state.cal_year += 1
    else:
        st.session_state.cal_month += 1
