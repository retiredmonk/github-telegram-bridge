import sqlite3, logging
from typing import Dict
from services.config_service import DB_FILE


def init_db ():

    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            message TEXT NOT NULL,
            SHA TEXT NOT NULL UNIQUE
        )
    """)

    connection.commit()

    return connection, cursor

def add_details (connection, data: Dict):
    cursor = connection.cursor()

    sha = data['sha']
    url = data['url']
    message = data['commit']['message']

    sql = '''INSERT INTO commits (url, message, SHA) VALUES (?, ?, ?)'''

    cursor.execute(sql, (url, message, sha))
    connection.commit()

    logging.info (f'DB insert successful')

def commit_status (connection, sha: str):
    cursor = connection.cursor()

    cursor.execute('''SELECT SHA FROM commits where SHA = ? LIMIT 1''', (sha,))
    return cursor.fetchone() is not None