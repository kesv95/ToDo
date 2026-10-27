
import os
import sqlite3
from pathlib import Path


# Vercel에서는 쓰기 가능한 임시 폴더를 사용하고,
# 로컬에서는 기존 데이터베이스 경로를 유지한다.
if os.getenv("VERCEL") == "1":
    DB_PATH = Path("/tmp/learning.db")
else:
    DB_PATH = Path(__file__).resolve().parent.parent / "learning.db"


def get_db():
    # 데이터베이스 폴더가 없으면 생성한다.
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """필요한 데이터베이스 테이블과 인덱스를 생성한다."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL DEFAULT '',
                email TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

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

        columns = {
            row["name"]
            for row in conn.execute(
                "PRAGMA table_info(learning_records)"
            ).fetchall()
        }

        if "user_id" not in columns:
            conn.execute("""
                ALTER TABLE learning_records
                ADD COLUMN user_id TEXT REFERENCES users(id)
            """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_learning_records_user_id_id
            ON learning_records(user_id, id DESC)
        """)


def save_user(user_id, name, email):
    """Google 계정 정보를 등록하거나 갱신한다."""
    with get_db() as conn:
        conn.execute("""
            INSERT INTO users (id, name, email)
            VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                email = excluded.email
        """, (user_id, name, email))


def get_records(user_id, limit=10):
    """특정 사용자의 학습진단 기록을 최신순으로 조회한다."""
    if not user_id:
        return []

    with get_db() as conn:
        return conn.execute("""
            SELECT *
            FROM learning_records
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
        """, (user_id, limit)).fetchall()


def save_record(
    user_id,
    category,
    study,
    plan,
    review,
    score,
    diagnosis,
    advice,
    created_at
):
    """학습진단 결과를 사용자에게 연결하여 저장한다."""
    if not user_id:
        raise ValueError("로그인한 사용자 ID가 필요합니다.")

    with get_db() as conn:
        conn.execute("""
            INSERT INTO learning_records (
                user_id,
                category,
                study,
                plan,
                review,
                score,
                diagnosis,
                advice,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            category,
            study,
            plan,
            review,
            score,
            diagnosis,
            advice,
            created_at
        ))


# Vercel은 앱을 가져올 때 테이블이 준비되도록 초기화한다.
init_db()
