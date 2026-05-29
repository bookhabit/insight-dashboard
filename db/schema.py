import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS apps (
            id           INTEGER PRIMARY KEY,
            name         TEXT,
            description  TEXT,
            category     TEXT,
            source       TEXT,
            framework    TEXT,
            url          TEXT UNIQUE,
            extra        TEXT,
            collected_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS bookmarks (
            id       INTEGER PRIMARY KEY,
            app_id   INTEGER NOT NULL,
            memo     TEXT DEFAULT '',
            tags     TEXT DEFAULT '',
            saved_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (app_id) REFERENCES apps(id)
        );

        CREATE TABLE IF NOT EXISTS daily_memos (
            id         INTEGER PRIMARY KEY,
            date       DATE UNIQUE,
            content    TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME
        );

        CREATE TABLE IF NOT EXISTS ideas (
            id                     INTEGER PRIMARY KEY,
            title                  TEXT NOT NULL,
            description            TEXT DEFAULT '',
            category               TEXT DEFAULT '',
            tags                   TEXT DEFAULT '',
            status                 TEXT DEFAULT 'new',
            source_date            DATE,
            lc_customer_segments   TEXT DEFAULT '',
            lc_value_proposition   TEXT DEFAULT '',
            lc_channels            TEXT DEFAULT '',
            lc_customer_relations  TEXT DEFAULT '',
            lc_revenue_streams     TEXT DEFAULT '',
            lc_key_resources       TEXT DEFAULT '',
            lc_key_activities      TEXT DEFAULT '',
            lc_key_partners        TEXT DEFAULT '',
            lc_cost_structure      TEXT DEFAULT '',
            created_at             DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at             DATETIME
        );
    """)
    conn.commit()
    conn.close()
