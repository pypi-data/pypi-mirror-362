# dualdb_memory/summarizer_base.py

from abc import ABC, abstractmethod
from typing import List, Tuple, Union

class BaseSummarizer(ABC):
    """摘要器接口：实现 summarize 方法即可插拔"""
    @abstractmethod
    def summarize(self, texts: List[str]) -> Union[str, Tuple[str, List[str]]]:
        """
        对一组文本进行摘要
        返回：
          - 纯文本摘要 str
          - 或 (摘要文本 str, 标签列表 List[str])
        """
        pass
