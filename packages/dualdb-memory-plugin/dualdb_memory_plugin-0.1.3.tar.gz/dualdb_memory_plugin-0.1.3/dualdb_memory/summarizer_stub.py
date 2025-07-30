# dualdb_memory/summarizer_stub.py

from .summarizer_base import BaseSummarizer
from typing import List, Tuple, Union

class StubSummarizer(BaseSummarizer):
    """默认的假摘要器，简单返回条数和首句示例"""
    def summarize(self, texts: List[str]) -> Union[str, Tuple[str, List[str]]]:
        if not texts:
            return "（空摘要）"
        summary = f"【摘要】共{len(texts)}句，首句：{texts[0][:20]}"
        return summary
