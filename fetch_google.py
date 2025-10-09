import os


try:
    from dotenv import load_dotenv

    dotenv_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        print("✅ Loaded environment variables from .env")
    else:
        print("⚠️ No .env file found, using existing environment settings.")
except Exception as e:
    print(f"⚠️ Could not load .env file: {e}")

import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from email_notify import send_email_with_html

DB_PATH = os.path.join(os.getcwd(), "scraper.db")


# -------------------------------------------
# Database Setup
# -------------------------------------------
def init_db(path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            date TEXT
        )
    """)
    conn.commit()
    return conn


# -------------------------------------------
# Fetch AI in Automation News
# -------------------------------------------
def fetch_articles():
    query = "AI in automation"
    url = f"https://news.google.com/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.select("article h3 a")[:10]:  # limit to top 10
        title = item.get_text()
        href = item["href"]
        if href.startswith("./"):
            href = "https://news.google.com" + href[1:]
        articles.append({"title": title, "url": href})
    return articles


# -------------------------------------------
# Simple Summarizer
# -------------------------------------------
def summarize_article(url, max_sentences=2):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        text = " ".join(paragraphs).strip()
        sentences = text.split(". ")
        summary = ". ".join(sentences[:max_sentences]) + "."
        return summary if len(summary) > 10 else "(No summary available)"
    except Exception as e:
        return f"(Could not summarize: {e})"


# -------------------------------------------
# Build HTML Email Layout
# -------------------------------------------
def generate_email_html(articles):
    html = """
    <html>
    <head>
    <style>
        body { font-family: 'Georgia', serif; background-color: #f8f9fa; color: #333; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #444; }
        .article { border-bottom: 1px solid #ddd; padding-bottom: 15px; margin-bottom: 15px; }
        .title { font-size: 1.2em; font-weight: bold; color: #2a7ae2; text-decoration: none; }
        .summary { margin-top: 8px; font-size: 0.95em; line-height: 1.5; }
        .footer { text-align: center; font-size: 0.8em; color: #999; margin-top: 20px; }
    </style>
    </head>
    <body>
    <div class="container">
    <h1>Daily AI in Automation Digest</h1>
    """

    for article in articles:
        html += f"""
        <div class="article">
            <a class="title" href="{article["url"]}">{article["title"]}</a>
            <p class="summary">{article["summary"]}</p>
        </div>
        """

    html += """
    <div class="footer">
        <p>Delivered automatically by your AI Scraper ✨</p>
    </div>
    </div>
    </body>
    </html>
    """
    return html


# -------------------------------------------
# Main Script
# -------------------------------------------
if __name__ == "__main__":
    conn = init_db(DB_PATH)
    c = conn.cursor()
    articles = fetch_articles()
    new_articles = []

    for a in articles:
        c.execute("SELECT * FROM articles WHERE url = ?", (a["url"],))
        if not c.fetchone():
            summary = summarize_article(a["url"])
            a["summary"] = summary
            c.execute(
                "INSERT INTO articles (title, url, date) VALUES (?, ?, ?)",
                (a["title"], a["url"], datetime.now().strftime("%Y-%m-%d")),
            )
            new_articles.append(a)
    conn.commit()
    conn.close()

    TEST_MODE = False  # Set to False when done testing

    if TEST_MODE:
        # Force email to send a preview with dummy articles
        new_articles = [
            {
                "title": "Test: AI Automation Revolution",
                "url": "https://example.com",
                "summary": "This is a simulated summary of how AI is changing automation.",
            },
            {
                "title": "Test: Machine Learning in Industry",
                "url": "https://example.com/ml",
                "summary": "Machine learning is enhancing process efficiency across sectors.",
            },
        ]

    if new_articles:
        html_email = generate_email_html(new_articles)
        send_email_with_html("Today's AI Automation Digest", html_email, DB_PATH)
    else:
        print("No new articles found today.")
