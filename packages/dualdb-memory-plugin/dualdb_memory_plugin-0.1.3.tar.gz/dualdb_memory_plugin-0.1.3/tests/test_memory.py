# tests/test_memory.py

import os
import json
import sqlite3
import tempfile
import pytest

from dualdb_memory.store_json import JsonStore
from dualdb_memory.store_sqlite import SQLiteStore
from dualdb_memory.summarizer_stub import StubSummarizer
from dualdb_memory.manager import DualDBManager

def test_json_store(tmp_path):
    fp = tmp_path / "test.json"
    store = JsonStore(str(fp))
    # 初始为空
    assert store.get_entries() == []

    # 添加条目
    store.add_entry("user", "hello", tags=["greet"])
    data = store.get_entries()
    assert len(data) == 1
    assert data[0]["role"] == "user"
    assert data[0]["content"] == "hello"
    assert data[0]["tags"] == ["greet"]

    # 清空
    store.clear()
    assert store.get_entries() == []

def test_sqlite_store(tmp_path):
    dbf = tmp_path / "test.db"
    store = SQLiteStore(f"sqlite:///{dbf}")
    # 初始为空
    assert store.get_entries() == []

    # 添加条目
    store.add_entry("assistant", "reply", tags=["info"])
    rows = store.get_entries()
    assert len(rows) == 1
    assert rows[0]["role"] == "assistant"
    assert rows[0]["content"] == "reply"
    assert rows[0]["tags"] == ["info"]

    # 清空
    store.clear()
    assert store.get_entries() == []

def test_dualdb_memory_rotation(tmp_path):
    # 使用 JSON 存储测试轮回逻辑
    active_fp = tmp_path / "a.json"
    archive_fp = tmp_path / "b.json"
    mgr = DualDBManager(
        storage_type="json",
        active_path=str(active_fp),
        archive_path=str(archive_fp),
        summarizer=StubSummarizer(),
        threshold=2,       # 2 条消息触发一次轮回
        keywords=None,
        time_delta=None
    )

    # 添加两条消息后会生成摘要到 archive
    mgr.append("user", "msg1")
    mgr.append("assistant", "msg2")
    # archive 上应有一条摘要
    arch = mgr.memory.archive_store.get_entries()
    assert len(arch) == 1
    assert "摘要" in arch[0]["content"]

    # active 已被清空
    active = mgr.memory.active_store.get_entries()
    assert active == []

def test_get_context_combines(tmp_path):
    # JSON 模式
    active_fp = tmp_path / "act.json"
    archive_fp = tmp_path / "arc.json"
    mgr = DualDBManager(
        storage_type="json",
        active_path=str(active_fp),
        archive_path=str(archive_fp),
        summarizer=StubSummarizer(),
        threshold=3
    )

    # 不触发摘要前，context 等于 active 列表
    mgr.append("user", "one")
    ctx1 = mgr.get_context()
    assert len(ctx1) == 1 and ctx1[0]["content"] == "one"

    # 触发一次摘要
    mgr.append("assistant", "two")
    mgr.append("user", "three")
    # 现在 archive 有一条摘要，active 清空
    ctx2 = mgr.get_context()
    assert len(ctx2) == 1 and ctx2[0]["role"] == "system"

    # 新增条目加入 active
    mgr.append("assistant", "four")
    ctx3 = mgr.get_context()
    # 长度应 archive(1) + active(1) = 2
    assert len(ctx3) == 2

if __name__ == "__main__":
    pytest.main()
