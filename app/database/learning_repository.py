import sqlite3
from pathlib import Path


# DB 파일 경로
DB_PATH = Path(__file__).resolve().parent.parent / "learning.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_db() as conn:
        # 1. 사용자 테이블 생성
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL DEFAULT '',
                email TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. 기존 학습 기록 테이블 생성
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

        # 3. 기존 테이블에 user_id 컬럼이 있는지 확인
        columns = {
            row["name"]
            for row in conn.execute(
                "PRAGMA table_info(learning_records)"
            ).fetchall()
        }

        # 4. user_id 컬럼이 없을 때만 추가
        if "user_id" not in columns:
            conn.execute("""
                ALTER TABLE learning_records
                ADD COLUMN user_id TEXT REFERENCES users(id)
            """)

        # 5. 사용자별 학습 기록 조회를 위한 인덱스 생성
        conn.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_learning_records_user_id_id
            ON learning_records(user_id, id DESC)
        """)


def save_user(user_id, name, email):
    """Google 계정 정보를 등록하거나 최신 정보로 갱신한다."""

    with get_db() as conn:
        conn.execute("""
            INSERT INTO users (id, name, email)
            VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                email = excluded.email
        """, (user_id, name, email))


def get_records(user_id, limit=10):
    """특정 사용자의 학습진단 기록만 최신순으로 조회한다."""

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
    """학습진단 결과를 해당 사용자에게 연결하여 저장한다."""

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