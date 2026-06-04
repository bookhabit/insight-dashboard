import html as _html
import json
import re
from db.schema import get_conn


def _strip_html(text: str) -> str:
    s = _html.unescape(text or "")
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.DOTALL)
    s = re.sub(r"<[^>]*>?", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def save_items(items: list[dict]) -> int:
    conn  = get_conn()
    saved = 0
    for item in items:
        url = (item.get("url") or "").strip()
        if not url:
            continue
        exists = conn.execute("SELECT id FROM apps WHERE url = ?", (url,)).fetchone()
        if exists:
            continue
        conn.execute(
            """INSERT INTO apps (name, description, category, source, framework, url, extra)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                _strip_html(item.get("name")        or "")[:200],
                _strip_html(item.get("description") or "")[:500],
                (item.get("category")    or ""),
                (item.get("source")      or ""),
                (item.get("framework")   or ""),
                url,
                json.dumps(item.get("extra") or {}, ensure_ascii=False),
            ),
        )
        saved += 1
    conn.commit()
    conn.close()
    return saved
