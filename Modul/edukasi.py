import sqlite3
import os

def get_articles():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Database', 'kampussecure.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT title, content FROM edukasi')
    rows = cursor.fetchall()
    articles = [{"title": row[0], "content": row[1]} for row in rows]
    conn.close()
    return articles
