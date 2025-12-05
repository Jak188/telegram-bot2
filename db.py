import sqlite3
from typing import Optional

class DB:
    def __init__(self, path="bot.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        username TEXT,
                        registered_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )""")
        self.conn.commit()

    def add_user(self, user_id:int, name:str, username:Optional[str]=None):
        cur = self.conn.cursor()
        cur.execute("INSERT OR REPLACE INTO users (id,name,username) VALUES (?,?,?)", (user_id,name,username))
        self.conn.commit()

    def user_exists(self, user_id:int) -> bool:
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE id=?", (user_id,))
        return cur.fetchone() is not None
