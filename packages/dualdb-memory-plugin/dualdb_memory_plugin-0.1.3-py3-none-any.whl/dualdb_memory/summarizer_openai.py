# dualdb_memory/summarizer_openai.py

import os
import openai
from typing import List, Tuple, Union
from .summarizer_base import BaseSummarizer

class OpenAISummarizer(BaseSummarizer):
    """
    基于 OpenAI ChatCompletion 的摘要器实现。
    依赖环境变量 OPENAI_API_KEY。
    """

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.3,
        api_key_env: str = "OPENAI_API_KEY"
    ):
        key = os.getenv(api_key_env)
        if not key:
            raise RuntimeError(f"Environment variable {api_key_env} is not set")
        openai.api_key = key
        self.model = model
        self.temperature = temperature

    def summarize(self, texts: List[str]) -> Union[str, Tuple[str, List[str]]]:
        prompt = "请将以下对话内容浓缩成一句话摘要：\n" + "\n".join(texts)
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature
        )
        return resp.choices[0].message.content.strip()
