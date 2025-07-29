import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'nanourls.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL UNIQUE,
            short_code TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    return conn

def insert_url(long_url, short_code):
    conn = get_db()
    conn.execute('INSERT INTO urls (long_url, short_code) VALUES (?, ?)', (long_url, short_code))
    conn.commit()
    conn.close()

def get_url_by_code(short_code):
    conn = get_db()
    cursor = conn.execute('SELECT * FROM urls WHERE short_code=?', (short_code,))
    return cursor.fetchone()

def get_url_by_long(long_url):
    conn = get_db()
    cursor = conn.execute('SELECT * FROM urls WHERE long_url=?', (long_url,))
    return cursor.fetchone()