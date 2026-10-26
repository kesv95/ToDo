import sqlite3
from pathlib import Path

# DB 파일 경로
DB_PATH = Path(__file__).resolve().parent.parent / "learning.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS learning_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category INTEGER NOT NULL,
                study INTEGER NOT NULL,
                plan INTEGER NOT NULL,
                review INTEGER NOT NULL,
                score INTEGER NOT NULL,
                diagnosis TEXT NOT NULL,
                advice TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def get_records():
    with get_db() as conn:
        return conn.execute("""
            SELECT *
            FROM learning_records
            ORDER BY id DESC
            LIMIT 10
        """).fetchall()


def save_record(
    category,
    study,
    plan,
    review,
    score,
    diagnosis,
    advice,
    created_at
):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO learning_records
            (category, study, plan, review,
             score, diagnosis, advice, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            category,
            study,
            plan,
            review,
            score,
            diagnosis,
            advice,
            created_at
        ))