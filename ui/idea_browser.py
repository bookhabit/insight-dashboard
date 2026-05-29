import streamlit as st
from services.idea import (
    add_idea, get_ideas, update_idea_status,
    update_lean_canvas, update_idea, delete_idea,
    lean_canvas_progress, LC_FIELDS,
)

STATUS_MAP = {
    "💡 새 아이디어": "new",
    "🔨 발전 중":    "developing",
    "✅ 완성":       "done",
    "🗑️ 보류":      "hold",
}
STATUS_LABEL = {v: k for k, v in STATUS_MAP.items()}

LC_META = [
    ("lc_customer_segments",  "1. 고객 세그먼트",  "이 서비스를 쓸 사람은 누구인가?"),
    ("lc_value_proposition",  "2. 가치 제안",      "고객에게 어떤 가치를 주는가?"),
    ("lc_channels",           "3. 채널",           "어떻게 고객에게 전달할 것인가?"),
    ("lc_customer_relations", "4. 고객 관계",      "고객과 어떤 관계를 유지할 것인가?"),
    ("lc_revenue_streams",    "5. 수익원",         "어떻게 돈을 벌 것인가?"),
    ("lc_key_resources",      "6. 핵심 자원",      "서비스 운영에 반드시 필요한 자원은?"),
    ("lc_key_activities",     "7. 핵심 활동",      "가장 중요하게 해야 할 활동은?"),
    ("lc_key_partners",       "8. 핵심 파트너",    "누구와 협력해야 하는가?"),
    ("lc_cost_structure",     "9. 비용 구조",      "주요 비용 항목은 무엇인가?"),
]


def render():
    st.title("💡 아이디어 컬렉션")

    _quick_add_form()
    st.divider()

    # 상태 필터 + 뷰 토글
    f_col, v_col = st.columns([7, 3])
    with f_col:
        status_label = st.radio(
            "상태",
            list(STATUS_MAP.keys()) + ["전체"],
            horizontal=True,
            index=4,
            label_visibility="collapsed",
        )
    with v_col:
        view_mode = st.radio("뷰", ["카드", "목록"], horizontal=True, label_visibility="collapsed")

    status_val = STATUS_MAP.get(status_label)
    ideas = get_ideas(status=status_val)

    if not ideas:
        st.info("저장된 아이디어가 없습니다.")
        return

    if view_mode == "카드":
        _card_browser(ideas)
    else:
        _list_view(ideas)


# ── Quick Add ────────────────────────────────────────────────────────────────

def _quick_add_form():
    promote_content = st.session_state.pop("promote_content", "")
    promote_date    = st.session_state.pop("promote_date", None)

    expanded = bool(promote_content)
    with st.expander("➕ 아이디어 빠르게 추가", expanded=expanded):
        title = st.text_input(
            "제목 *",
            value=promote_content[:60] if promote_content else "",
            placeholder="아이디어 제목",
        )
        desc = st.text_area(
            "메모",
            value=promote_content if promote_content else "",
            height=80,
            placeholder="떠오른 생각을 간단히 메모",
        )
        c1, c2 = st.columns(2)
        with c1:
            tags = st.text_input("태그", placeholder="#루틴 #감정 #리텐션")
        with c2:
            category = st.text_input("카테고리", placeholder="앱 아이디어")

        if st.button("💾 저장", key="quick_add_save"):
            if title.strip():
                add_idea(
                    title=title.strip(),
                    description=desc,
                    category=category,
                    tags=tags,
                    source_date=promote_date,
                )
                st.success("저장됐습니다!")
                st.rerun()
            else:
                st.warning("제목을 입력해주세요.")


# ── Card Browser ─────────────────────────────────────────────────────────────

def _card_browser(ideas: list[dict]):
    if "idea_index" not in st.session_state:
        st.session_state.idea_index = 0

    # 인덱스 범위 보정
    st.session_state.idea_index = min(st.session_state.idea_index, len(ideas) - 1)
    idx  = st.session_state.idea_index
    idea = ideas[idx]

    # 네비게이션
    n1, n2, n3 = st.columns([2, 6, 2])
    with n1:
        if st.button("← 이전", disabled=idx == 0, use_container_width=True):
            st.session_state.idea_index -= 1
            st.rerun()
    with n2:
        st.markdown(
            f"<div style='text-align:center;padding:6px;color:#888'>{idx+1} / {len(ideas)}</div>",
            unsafe_allow_html=True,
        )
    with n3:
        if st.button("다음 →", disabled=idx == len(ideas) - 1, use_container_width=True):
            st.session_state.idea_index += 1
            st.rerun()

    # 카드
    filled, total = lean_canvas_progress(idea)
    with st.container(border=True):
        st.markdown(f"### {idea['title']}")
        if idea.get("tags"):
            tags_str = " ".join(
                f"`#{t.strip('#').strip()}`" for t in idea["tags"].replace(",", " ").split() if t.strip()
            )
            st.markdown(tags_str)
        if idea.get("description"):
            st.write(idea["description"])
        if idea.get("source_date"):
            st.caption(f"📅 {idea['source_date']} 메모에서")

        st.progress(filled / 9, text=f"린 캔버스 {filled}/9")

        # 상태 버튼
        s_cols = st.columns(4)
        for i, (label, val) in enumerate(STATUS_MAP.items()):
            with s_cols[i]:
                is_cur = idea["status"] == val
                if st.button(
                    label,
                    key=f"status_{idea['id']}_{val}",
                    type="primary" if is_cur else "secondary",
                    use_container_width=True,
                ):
                    update_idea_status(idea["id"], val)
                    st.rerun()

    # 린 캔버스
    with st.expander("🗂️ 린 캔버스 디벨롭 체크리스트"):
        _lean_canvas_form(idea)

    # 삭제
    with st.expander("⚙️ 편집 / 삭제"):
        _edit_form(idea)


# ── Lean Canvas Form ──────────────────────────────────────────────────────────

def _lean_canvas_form(idea: dict):
    updated = {}
    for field, label, placeholder in LC_META:
        val = st.text_area(
            label,
            value=idea.get(field) or "",
            placeholder=placeholder,
            height=90,
            key=f"lc_{idea['id']}_{field}",
        )
        updated[field] = val

    if st.button("💾 린 캔버스 저장", key=f"save_lc_{idea['id']}"):
        update_lean_canvas(idea["id"], updated)
        st.success("저장됐습니다!")
        st.rerun()


# ── Edit Form ─────────────────────────────────────────────────────────────────

def _edit_form(idea: dict):
    new_title = st.text_input("제목", value=idea["title"], key=f"edit_title_{idea['id']}")
    new_desc  = st.text_area("메모", value=idea.get("description", ""), height=80, key=f"edit_desc_{idea['id']}")
    new_tags  = st.text_input("태그", value=idea.get("tags", ""), key=f"edit_tags_{idea['id']}")
    new_cat   = st.text_input("카테고리", value=idea.get("category", ""), key=f"edit_cat_{idea['id']}")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("💾 수정 저장", key=f"edit_save_{idea['id']}", use_container_width=True):
            update_idea(idea["id"], new_title, new_desc, new_tags, new_cat)
            st.success("수정됐습니다.")
            st.rerun()
    with c2:
        if st.button("🗑 삭제", key=f"delete_{idea['id']}", use_container_width=True, type="primary"):
            delete_idea(idea["id"])
            st.session_state.idea_index = max(0, st.session_state.idea_index - 1)
            st.rerun()


# ── List View ─────────────────────────────────────────────────────────────────

def _list_view(ideas: list[dict]):
    for idea in ideas:
        filled, _ = lean_canvas_progress(idea)
        status_lbl = STATUS_LABEL.get(idea["status"], idea["status"])
        with st.container(border=True):
            c1, c2 = st.columns([8, 2])
            with c1:
                st.markdown(f"**{idea['title']}**")
                meta = f"{status_lbl} &nbsp;·&nbsp; 린캔버스 {filled}/9"
                if idea.get("tags"):
                    meta += f" &nbsp;·&nbsp; {idea['tags']}"
                st.caption(meta)
            with c2:
                if st.button("열기", key=f"open_{idea['id']}", use_container_width=True):
                    all_ids = [i["id"] for i in get_ideas()]
                    if idea["id"] in all_ids:
                        st.session_state.idea_index = all_ids.index(idea["id"])
                    st.session_state["idea_view_mode_override"] = "카드"
                    st.rerun()
