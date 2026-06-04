from db.schema import get_conn


def add_bookmark(app_id: int, memo: str = "", tags: str = "") -> int:
    conn = get_conn()
    exists = conn.execute("SELECT id FROM bookmarks WHERE app_id = ?", (app_id,)).fetchone()
    if exists:
        conn.close()
        return exists["id"]
    cursor = conn.execute(
        "INSERT INTO bookmarks (app_id, memo, tags) VALUES (?, ?, ?)",
        (app_id, memo, tags),
    )
    bm_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return bm_id


def remove_bookmark(app_id: int):
    conn = get_conn()
    conn.execute("DELETE FROM bookmarks WHERE app_id = ?", (app_id,))
    conn.commit()
    conn.close()


def update_bookmark(bm_id: int, memo: str, tags: str):
    conn = get_conn()
    conn.execute(
        "UPDATE bookmarks SET memo = ?, tags = ? WHERE id = ?",
        (memo, tags, bm_id),
    )
    conn.commit()
    conn.close()


def is_bookmarked(app_id: int) -> bool:
    conn = get_conn()
    row  = conn.execute("SELECT id FROM bookmarks WHERE app_id = ?", (app_id,)).fetchone()
    conn.close()
    return row is not None


def get_all_bookmarks() -> list[dict]:
    conn = get_conn()
    rows = conn.execute("""
        SELECT b.id, b.app_id, b.memo, b.tags, b.saved_at,
               a.name, a.description, a.source, a.framework, a.url, a.category
        FROM bookmarks b
        JOIN apps a ON b.app_id = a.id
        ORDER BY b.saved_at DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]
