import sqlite3
import os
from datetime import datetime

DB = os.path.expanduser("~") + "/FRIDAY/memory/friday.db"

def init():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memory
                 (id INTEGER PRIMARY KEY,
                  key TEXT,
                  value TEXT,
                  time TEXT)''')
    conn.commit()
    conn.close()

def remember(key, value):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO memory (key,value,time) VALUES (?,?,?)",
              (key, value, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def recall(key):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT value FROM memory WHERE key=? ORDER BY id DESC LIMIT 1", (key,))
    r = c.fetchone()
    conn.close()
    return r[0] if r else None

init()