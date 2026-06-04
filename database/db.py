import sqlite3
from pathlib import Path
from typing import Dict

FILE_PATH = Path("database/commits.db")


def get_connection():
    FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(FILE_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS commits (
                sha TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)


def add_details(data: Dict) -> bool:
    sha = data['sha']
    url = data['html_url']
    message = data['commit']['message']

    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO commits (sha, url, message)
                VALUES (?, ?, ?)
                """,
                (sha, url, message)
            )
        return True

    except sqlite3.IntegrityError:
        return False


def commit_status(sha: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT 1 FROM commits WHERE sha = ? LIMIT 1",
            (sha,)
        )
        return cursor.fetchone() is not None