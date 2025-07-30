# dualdb_memory/memory.py

import time
from typing import Any, List, Optional, Tuple, Union
from .store_json import JsonStore
from .store_sqlite import SQLiteStore
from .summarizer_base import BaseSummarizer

class DualDBMemory:
    """
    双数据库轮回记忆核心类：
      - active_store: 热存储（消息累积）
      - archive_store: 冷存储（摘要累积）
      - summarizer: 摘要器实例
      - trigger 条件：threshold, keywords, time_delta
    """
    def __init__(
        self,
        active_store: Any,
        archive_store: Any,
        summarizer: BaseSummarizer,
        threshold: int = 10,
        keywords: Optional[List[str]] = None,
        time_delta: Optional[float] = None,
    ):
        self.active_store = active_store
        self.archive_store = archive_store
        self.summarizer = summarizer
        self.threshold = threshold
        self.keywords = keywords or []
        self.time_delta = time_delta
        self.last_summary_time = time.time()

    def append(self, role: str, content: str) -> None:
        """添加一条对话并触发轮回检查"""
        self.active_store.add_entry(role, content)
        self._check_and_rotate()

    def _check_and_rotate(self) -> None:
        """检查触发条件并执行摘要轮回"""
        msgs = self.active_store.get_entries()
        trigger = False

        # 条数触发
        if len(msgs) >= self.threshold:
            trigger = True

        # 关键词触发
        if any(kw in entry['content'] for entry in msgs for kw in self.keywords):
            trigger = True

        # 时间间隔触发
        if self.time_delta is not None and (time.time() - self.last_summary_time) >= self.time_delta:
            trigger = True

        if trigger:
            # 将所有 active 消息拼接为文本列表
            texts = [f"{e['role']}: {e['content']}" for e in msgs]

            # 调用摘要器
            result = self.summarizer.summarize(texts)
            if isinstance(result, tuple):
                summary_text, tags = result
            else:
                summary_text, tags = result, []

            # 存入 archive
            self.archive_store.add_entry(role='system', content=summary_text, tags=tags)

            # 清空 active，并重置时间戳
            self.active_store.clear()
            self.last_summary_time = time.time()

    def get_context(self) -> List[dict]:
        """
        返回当前上下文条目列表，
        先 archive （历史摘要），再 active（当前消息）
        """
        archive = self.archive_store.get_entries()
        active = self.active_store.get_entries()
        return archive + active
