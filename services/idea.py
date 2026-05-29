from datetime import datetime
from db.schema import get_conn

LC_FIELDS = [
    "lc_customer_segments",
    "lc_value_proposition",
    "lc_channels",
    "lc_customer_relations",
    "lc_revenue_streams",
    "lc_key_resources",
    "lc_key_activities",
    "lc_key_partners",
    "lc_cost_structure",
]


def add_idea(title: str, description: str = "", category: str = "",
             tags: str = "", source_date: str = None) -> int:
    conn   = get_conn()
    cursor = conn.execute(
        "INSERT INTO ideas (title, description, category, tags, source_date) VALUES (?, ?, ?, ?, ?)",
        (title, description, category, tags, source_date),
    )
    idea_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return idea_id


def get_ideas(status: str = None) -> list[dict]:
    conn = get_conn()
    if status:
        rows = conn.execute(
            "SELECT * FROM ideas WHERE status = ? ORDER BY created_at DESC", (status,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM ideas ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_idea(idea_id: int) -> dict | None:
    conn = get_conn()
    row  = conn.execute("SELECT * FROM ideas WHERE id = ?", (idea_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_idea_status(idea_id: int, status: str):
    conn = get_conn()
    conn.execute(
        "UPDATE ideas SET status = ?, updated_at = ? WHERE id = ?",
        (status, datetime.now().isoformat(), idea_id),
    )
    conn.commit()
    conn.close()


def update_lean_canvas(idea_id: int, fields: dict):
    valid  = {k: v for k, v in fields.items() if k in LC_FIELDS}
    if not valid:
        return
    set_clause = ", ".join(f"{k} = ?" for k in valid)
    values     = list(valid.values()) + [datetime.now().isoformat(), idea_id]
    conn       = get_conn()
    conn.execute(f"UPDATE ideas SET {set_clause}, updated_at = ? WHERE id = ?", values)
    conn.commit()
    conn.close()


def update_idea(idea_id: int, title: str, description: str, tags: str, category: str):
    conn = get_conn()
    conn.execute(
        "UPDATE ideas SET title=?, description=?, tags=?, category=?, updated_at=? WHERE id=?",
        (title, description, tags, category, datetime.now().isoformat(), idea_id),
    )
    conn.commit()
    conn.close()


def delete_idea(idea_id: int):
    conn = get_conn()
    conn.execute("DELETE FROM ideas WHERE id = ?", (idea_id,))
    conn.commit()
    conn.close()


def lean_canvas_progress(idea: dict) -> tuple[int, int]:
    filled = sum(1 for f in LC_FIELDS if idea.get(f))
    return filled, 9
