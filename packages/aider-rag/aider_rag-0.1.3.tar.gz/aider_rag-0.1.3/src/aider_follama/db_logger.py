# aider_rag/db_logger.py

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.expanduser("~/aider_rag_queries.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS rag_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            query TEXT,
            context TEXT,
            ollama_response TEXT,
            aider_response TEXT
        )''')
        conn.commit()

def log_query_response(query, context, ollama_response, aider_response):
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO rag_logs (timestamp, query, context, ollama_response, aider_response)
                     VALUES (?, ?, ?, ?, ?)''',
                  (datetime.now().isoformat(), query, context, ollama_response, aider_response))
        conn.commit()
