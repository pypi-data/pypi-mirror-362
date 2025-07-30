# dualdb_memory/store_sqlite.py

import os
import sqlite3
from threading import Lock
from typing import Any, Dict, List, Optional

class SQLiteStore:
    """
    基于 SQLite 文件的存储适配器。
    表 schema: entries(id INTEGER PRIMARY KEY, role TEXT, content TEXT, tags TEXT)
    tags 以 JSON 字符串形式存储，可选
    """
    def __init__(self, db_path: str):
        self.db_path = db_path.replace("sqlite:///", "")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.lock = Lock()
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        with self.lock:
            cur = self.conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    tags TEXT
                )
            """)
            self.conn.commit()

    def add_entry(self, role: str, content: str, tags: Optional[List[str]] = None) -> None:
        """向 SQLite 写入一条条目"""
        tags_json = None
        if tags:
            import json
            tags_json = json.dumps(tags, ensure_ascii=False)
        with self.lock:
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO entries(role, content, tags) VALUES (?, ?, ?)",
                (role, content, tags_json)
            )
            self.conn.commit()

    def get_entries(self) -> List[Dict[str, Any]]:
        """读取并返回所有条目列表"""
        with self.lock:
            cur = self.conn.cursor()
            cur.execute("SELECT role, content, tags FROM entries ORDER BY id")
            rows = cur.fetchall()

        result = []
        for role, content, tags_json in rows:
            entry: Dict[str, Any] = {"role": role, "content": content}
            if tags_json:
                import json
                entry["tags"] = json.loads(tags_json)
            result.append(entry)
        return result

    def clear(self) -> None:
        """清空所有条目"""
        with self.lock:
            cur = self.conn.cursor()
            cur.execute("DELETE FROM entries")
            self.conn.commit()
