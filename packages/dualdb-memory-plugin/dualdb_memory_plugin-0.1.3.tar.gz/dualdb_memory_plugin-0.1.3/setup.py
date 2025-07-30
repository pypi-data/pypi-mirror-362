# setup.py

from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent

# 读取 README.md
long_description = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="dualdb-memory-plugin",
    version="0.1.3",
    description="Lightweight AI dialogue memory rotation plugin with dual DB (JSON/SQLite) and pluggable summarizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="YZXY6151",
    author_email="yzxy6151@gmail.com",
    url="https://github.com/YZXY6151/dualdb-memory-plugin",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        # 如果需要 OpenAI 摘要，则取消注释下面一行
        # "openai>=0.27.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "console_scripts": [
            "dualdb-demo=dualdb_memory.cli:main",
        ],
    },
)


# # 在项目根目录执行
# pip install -e .

# # 之后可以直接运行示例
# dualdb-demo
