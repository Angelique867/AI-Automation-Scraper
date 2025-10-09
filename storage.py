import sqlite3
from typing import Iterable, Dict

def init_db(path="scraper.db"):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("""
      CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY,
        source TEXT,
        title TEXT,
        url TEXT UNIQUE,
        published TEXT,
        summary TEXT
      )
    """)
    conn.commit()
    return conn


def save_new_articles(conn, source: str, items: Iterable[Dict]) -> list:
    """
       Save articles to the database if their URL isn't already there.
       Returns a list of newly added articles.
       """
    cur = conn.cursor()
    new = []
    for it in items:
        try:
            cur.execute(
                "INSERT INTO articles (source, title, url, published, summary) VALUES (?,?,?,?,?)",
                (source, it["title"], it["link"], it.get("published",""), it.get("summary",""))
            )
            conn.commit()
            new.append(it)
        except sqlite3.IntegrityError:
            # URL already exists ->skip
            pass
    return new