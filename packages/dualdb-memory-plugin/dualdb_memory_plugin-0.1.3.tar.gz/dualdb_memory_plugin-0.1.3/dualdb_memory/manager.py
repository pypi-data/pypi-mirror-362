# dualdb_memory/manager.py

import time
from typing import List, Optional
from .memory import DualDBMemory
from .store_json import JsonStore
from .store_sqlite import SQLiteStore
from .summarizer_base import BaseSummarizer

class DualDBManager:
    """
    双数据库管理器：
      - active 和 archive 各持有一个存储实例
      - append()/get_context() 代理到当前 active 的 DualDBMemory
      - 支持 JSON 或 SQLite 两种存储后端
    """
    def __init__(
        self,
        storage_type: str = "json",
        active_path: str = "active.json",
        archive_path: str = "archive.json",
        summarizer: BaseSummarizer = None,
        threshold: int = 10,
        keywords: Optional[List[str]] = None,
        time_delta: Optional[float] = None,
    ):
        # 选择存储适配器
        if storage_type == "sqlite":
            active_store = SQLiteStore(f"sqlite:///{active_path}")
            archive_store = SQLiteStore(f"sqlite:///{archive_path}")
        else:
            active_store = JsonStore(active_path)
            archive_store = JsonStore(archive_path)

        # 创建 DualDBMemory
        self.memory = DualDBMemory(
            active_store=active_store,
            archive_store=archive_store,
            summarizer=summarizer,
            threshold=threshold,
            keywords=keywords,
            time_delta=time_delta
        )

    def append(self, role: str, content: str) -> None:
        """添加一条记录到 active，并可能触发轮回"""
        self.memory.append(role, content)

    def get_context(self) -> List[dict]:
        """返回 archive + active 的合并上下文"""
        return self.memory.get_context()

    def clear_all(self) -> None:
        """重置所有存储（active & archive）"""
        self.memory.active_store.clear()
        self.memory.archive_store.clear()
