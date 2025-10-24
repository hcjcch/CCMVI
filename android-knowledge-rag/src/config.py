"""
Android知识库RAG系统配置
"""
import os
from pathlib import Path

# 基础路径配置
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
KNOWLEDGE_DIR = Path(__file__).parent.parent.parent / "components"

# ChromaDB配置
CHROMA_PATH = DATA_DIR / "chroma_db"
COLLECTION_NAME = "android_knowledge"

# 嵌入模型配置
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 轻量级多语言模型，支持中文

# 检索配置
DEFAULT_TOP_K = 5
SIMILARITY_THRESHOLD = 0.7

# 支持的文件类型
SUPPORTED_EXTENSIONS = {'.md', '.txt', '.pdf'}

# 检索粒度模式
GRANULARITY_FILE = "file"      # 文件级别
GRANULARITY_PARAGRAPH = "paragraph"  # 段落级别
GRANULARITY_SENTENCE = "sentence"    # 句子级别
DEFAULT_GRANULARITY = GRANULARITY_FILE