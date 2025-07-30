# dualdb_memory/store_json.py

import json
import os
from threading import Lock
from typing import Any, Dict, List, Optional

class JsonStore:
    """
    基于 JSON 文件的存储适配器。
    每条条目格式为：{"role": str, "content": str, "tags": Optional[List[str]]}
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lock = Lock()
        # 初始化或清空文件
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    def add_entry(self, role: str, content: str, tags: Optional[List[str]] = None) -> None:
        """追加一条条目到 JSON 文件末尾"""
        entry: Dict[str, Any] = {"role": role, "content": content}
        if tags:
            entry["tags"] = tags

        with self.lock:
            data = self._read_all()
            data.append(entry)
            self._write_all(data)

    def get_entries(self) -> List[Dict[str, Any]]:
        """读取并返回所有条目列表"""
        with self.lock:
            return self._read_all()

    def clear(self) -> None:
        """清空所有条目"""
        with self.lock:
            self._write_all([])

    def _read_all(self) -> List[Dict[str, Any]]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _write_all(self, data: List[Dict[str, Any]]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
