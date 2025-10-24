"""
向量数据库管理器 - 基于ChromaDB实现
"""
import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from config import CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL, DEFAULT_TOP_K

class VectorStore:
    """向量数据库管理器"""

    def __init__(self, reset_db: bool = False):
        """
        初始化向量数据库

        Args:
            reset_db: 是否重置数据库
        """
        self.chroma_path = CHROMA_PATH
        self.collection_name = COLLECTION_NAME
        self.embedding_model = EMBEDDING_MODEL

        # 如果需要重置数据库
        if reset_db and self.chroma_path.exists():
            shutil.rmtree(self.chroma_path)
            print(f"🗑️  已清除旧的向量数据库")

        # 初始化ChromaDB
        self._init_chromadb()

        # 初始化嵌入模型
        self._init_embedding_model()

    def _init_chromadb(self):
        """初始化ChromaDB"""
        # 确保数据目录存在
        self.chroma_path.mkdir(parents=True, exist_ok=True)

        # 创建ChromaDB客户端
        self.client = chromadb.PersistentClient(
            path=str(self.chroma_path),
            settings=Settings(allow_reset=True)
        )

        # 获取或创建集合
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            print(f"✅ 已连接到现有集合: {self.collection_name}")
            print(f"📊 集合中有 {self.collection.count()} 个文档")
        except Exception:
            self.collection = self.client.create_collection(name=self.collection_name)
            print(f"🆕 创建新集合: {self.collection_name}")

    def _init_embedding_model(self):
        """初始化嵌入模型"""
        print(f"🔄 加载嵌入模型: {self.embedding_model}")
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=self.embedding_model
        )
        print(f"✅ 嵌入模型加载完成")

    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        添加文档到向量数据库

        Args:
            documents: 文档列表，每个文档包含content和metadata
        """
        if not documents:
            print("⚠️  没有文档需要添加")
            return

        # 准备数据
        ids = []
        texts = []
        metadatas = []

        for i, doc in enumerate(documents):
            # 生成唯一ID
            doc_id = doc['metadata']['chunk_id']
            ids.append(doc_id)

            # 文档内容
            texts.append(doc['content'])

            # 元数据
            metadatas.append(doc['metadata'])

        try:
            # 批量添加文档
            self.collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )
            print(f"✅ 成功添加 {len(documents)} 个文档到向量数据库")
            print(f"📊 数据库现在有 {self.collection.count()} 个文档")
        except Exception as e:
            print(f"❌ 添加文档失败: {e}")

    def search(self, query: str, top_k: int = DEFAULT_TOP_K, where: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        在向量数据库中搜索相似文档

        Args:
            query: 查询字符串
            top_k: 返回结果数量
            where: 元数据过滤条件

        Returns:
            搜索结果列表
        """
        try:
            # 构建查询参数
            query_params = {
                "query_texts": [query],
                "n_results": top_k
            }

            # 添加过滤条件
            if where:
                query_params["where"] = where

            # 执行搜索
            results = self.collection.query(**query_params)

            # 格式化结果
            formatted_results = []
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })

            return formatted_results

        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return []

    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        根据ID获取文档

        Args:
            doc_id: 文档ID

        Returns:
            文档内容或None
        """
        try:
            results = self.collection.get(ids=[doc_id])
            if results['ids']:
                return {
                    'id': results['ids'][0],
                    'content': results['documents'][0],
                    'metadata': results['metadatas'][0]
                }
        except Exception as e:
            print(f"❌ 获取文档失败: {e}")
        return None

    def get_stats(self) -> Dict[str, Any]:
        """获取数据库统计信息"""
        try:
            count = self.collection.count()
            return {
                'total_documents': count,
                'collection_name': self.collection_name,
                'embedding_model': self.embedding_model,
                'db_path': str(self.chroma_path)
            }
        except Exception as e:
            print(f"❌ 获取统计信息失败: {e}")
            return {}

    def reset_database(self):
        """重置数据库"""
        try:
            self.client.reset()
            print("🗑️  数据库已重置")
        except Exception as e:
            print(f"❌ 重置数据库失败: {e}")