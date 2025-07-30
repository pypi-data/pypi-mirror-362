# examples/demo_openai.py

import os
import openai
from dualdb_memory.manager import DualDBManager
from dualdb_memory.summarizer_openai import OpenAISummarizer

def chat_with_openai(prompt: str) -> str:
    """用 OpenAI API 生成 AI 回复"""
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return resp.choices[0].message.content.strip()

def main():
    # 1. 检查 API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ 请先设置环境变量 OPENAI_API_KEY")
        return
    openai.api_key = api_key

    # 2. 初始化轮回管理器
    mgr = DualDBManager(
        storage_type="json",
        active_path="data/active_openai.json",
        archive_path="data/archive_openai.json",
        summarizer=OpenAISummarizer(model="gpt-3.5-turbo", temperature=0.3),
        threshold=3
    )

    # 3. 模拟对话
    user_msgs = [
        "你好，你是谁？",
        "请帮我写一段Python代码。",
        "能解释一下这个插件的工作原理吗？",
        "最后再给我一段结论。"
    ]

    for msg in user_msgs:
        # a) 记录用户输入
        mgr.append("user", msg)

        # b) 构造提示：先把历史摘要和 active 拼接
        history = mgr.get_context()
        prompt_lines = []
        for entry in history:
            prompt_lines.append(f"{entry['role']}: {entry['content']}")
        # 加上本轮用户提问
        prompt_lines.append(f"user: {msg}")
        prompt_lines.append("assistant:")
        prompt = "\n".join(prompt_lines)

        # c) 调用 OpenAI 生成真实回答
        ai_reply = chat_with_openai(prompt)

        # d) 记录 AI 回复
        mgr.append("assistant", ai_reply)

        # e) 打印当前状态
        print("🗨️ 用户：", msg)
        print("🤖 AI：", ai_reply)
        print("🧠 当前上下文：")
        for entry in mgr.get_context():
            role = entry["role"]
            content = entry["content"]
            print(f"  {role}: {content}")
        print("-" * 50)

if __name__ == "__main__":
    main()


# python -m examples.demo_openai