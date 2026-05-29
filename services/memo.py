from datetime import datetime
from db.schema import get_conn


def get_memo(date: str) -> str:
    conn = get_conn()
    row  = conn.execute("SELECT content FROM daily_memos WHERE date = ?", (date,)).fetchone()
    conn.close()
    return row["content"] if row else ""


def save_memo(date: str, content: str):
    conn = get_conn()
    now  = datetime.now().isoformat()
    conn.execute("""
        INSERT INTO daily_memos (date, content, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET content = excluded.content, updated_at = excluded.updated_at
    """, (date, content, now))
    conn.commit()
    conn.close()


def get_memo_dates(year: int, month: int) -> set[str]:
    prefix = f"{year:04d}-{month:02d}-"
    conn   = get_conn()
    rows   = conn.execute(
        "SELECT date FROM daily_memos WHERE date LIKE ? AND content != ''",
        (prefix + "%",),
    ).fetchall()
    conn.close()
    return {row["date"] for row in rows}


def get_recent_memos(limit: int = 7) -> list[dict]:
    conn = get_conn()
    rows = conn.execute(
        "SELECT date, content FROM daily_memos WHERE content != '' ORDER BY date DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
