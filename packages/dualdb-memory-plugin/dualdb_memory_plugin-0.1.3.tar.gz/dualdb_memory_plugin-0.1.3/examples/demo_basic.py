# examples/demo_basic.py

from dualdb_memory.manager import DualDBManager
from dualdb_memory.summarizer_stub import StubSummarizer

def main():
    # 初始化 manager（JSON 存储，阈值 3）
    # mgr = DualDBManager(
    #     storage_type="json",
    #     active_path="active.json",
    #     archive_path="archive.json",
    #     summarizer=StubSummarizer(),
    #     threshold=3
    # )

    mgr = DualDBManager(
    storage_type="sqlite",
    active_path="data/active.db",
    archive_path="data/archive.db",
    summarizer=StubSummarizer(),
    threshold=3
)
    


    # 模拟对话
    user_msgs = [
        "你好，你是谁？",
        "你能帮我写一段Python代码吗？",
        "请给我一个倒序排列的函数示例",
        "再帮我解释一下它的复杂度"
    ]

    for msg in user_msgs:
        mgr.append("user", msg)
        # 获取上下文并模拟 AI 回复
        ctx = mgr.get_context()
        ai_reply = f"（假AI回复）收到“{msg[:10]}...”"
        mgr.append("assistant", ai_reply)

        # 打印当前状态
        print("🗨️ 用户：", msg)
        print("🤖 AI：", ai_reply)
        print("🧠 上下文：")
        for entry in ctx:
            role = entry["role"]
            content = entry["content"]
            print(f"  {role}: {content}")
        print("-" * 50)

if __name__ == "__main__":
    main()
