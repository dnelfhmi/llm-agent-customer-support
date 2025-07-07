import sqlite3
import json

conn = sqlite3.connect("memory.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ticket_memory (
    ticket_id TEXT PRIMARY KEY,
    messages TEXT
)
""")
conn.commit()

def save_memory(ticket_id, messages):
    cursor.execute(
        "REPLACE INTO ticket_memory (ticket_id, messages) VALUES (?, ?)",
        (ticket_id, json.dumps(messages))
    )
    conn.commit()

def load_memory(ticket_id):
    cursor.execute(
        "SELECT messages FROM ticket_memory WHERE ticket_id = ?",
        (ticket_id,)
    )
    row = cursor.fetchone()
    if row:
        return json.loads(row[0])
    return []
