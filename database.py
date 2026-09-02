# All the SQLite logic for our Feedback Analyzer lives here.

import sqlite3
from datetime import datetime
from config import DB_PATH


def init_db():
    """
    Create the reviews table if it doesn't already exist.
    Call this once when the app starts.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review_text TEXT NOT NULL,
            category TEXT,
            sentiment_label TEXT,
            sentiment_score REAL,
            date_added TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_review(review_text, category, sentiment_label, sentiment_score):
    """
    Save one analyzed review into the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO reviews (review_text, category, sentiment_label, sentiment_score, date_added)
        VALUES (?, ?, ?, ?, ?)
        """,
        (review_text, category, sentiment_label, sentiment_score, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_all_reviews():
    """
    Fetch every review currently stored, as a list of dictionaries.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us read columns by name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def clear_all_reviews():
    """
    Wipe the table clean. Handy when re-testing with fresh sample data.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reviews")
    conn.commit()
    conn.close()