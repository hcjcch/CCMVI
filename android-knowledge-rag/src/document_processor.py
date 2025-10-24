"""
文档处理器 - 支持不同粒度的文档分块处理
"""
import os
import re
from pathlib import Path
from typing import List, Dict, Any
import markdown
from config import SUPPORTED_EXTENSIONS, GRANULARITY_FILE, GRANULARITY_PARAGRAPH, GRANULARITY_SENTENCE

class DocumentProcessor:
    """文档处理器，支持文件级别、段落级别、句子级别的分块"""

    def __init__(self, granularity: str = GRANULARITY_FILE):
        self.granularity = granularity

    def load_documents(self, knowledge_dir: Path) -> List[Dict[str, Any]]:
        """
        从指定目录加载所有支持的文档

        Args:
            knowledge_dir: 知识库目录路径

        Returns:
            文档列表，每个文档包含内容和元数据
        """
        documents = []

        # 遍历所有支持的文件
        for file_path in knowledge_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                try:
                    # 读取文件内容
                    content = file_path.read_text(encoding='utf-8')

                    # 根据粒度设置分块
                    chunks = self._chunk_document(content, file_path)
                    documents.extend(chunks)

                    print(f"✅ 已处理文件: {file_path.name} ({len(chunks)} 个分块)")

                except Exception as e:
                    print(f"❌ 处理文件失败 {file_path}: {e}")

        return documents

    def _chunk_document(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """
        根据粒度设置对文档进行分块

        Args:
            content: 文档内容
            file_path: 文件路径

        Returns:
            分块列表
        """
        if self.granularity == GRANULARITY_FILE:
            return self._chunk_by_file(content, file_path)
        elif self.granularity == GRANULARITY_PARAGRAPH:
            return self._chunk_by_paragraph(content, file_path)
        elif self.granularity == GRANULARITY_SENTENCE:
            return self._chunk_by_sentence(content, file_path)
        else:
            raise ValueError(f"不支持的粒度设置: {self.granularity}")

    def _chunk_by_file(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """文件级别分块 - 整个文件作为一个分块"""
        # 如果是markdown文件，提取标题作为元数据
        metadata = self._extract_metadata(content, file_path)

        return [{
            'content': content.strip(),
            'metadata': {
                **metadata,
                'chunk_id': f"{file_path.stem}_whole",
                'chunk_type': 'file',
                'file_path': str(file_path.relative_to(file_path.parent.parent))
            }
        }]

    def _chunk_by_paragraph(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """段落级别分块 - 按空行分块"""
        # 提取基本元数据
        base_metadata = self._extract_metadata(content, file_path)

        # 分割段落（按空行分割）
        paragraphs = re.split(r'\n\s*\n', content.strip())
        chunks = []

        for i, paragraph in enumerate(paragraphs):
            if paragraph.strip():  # 忽略空段落
                chunks.append({
                    'content': paragraph.strip(),
                    'metadata': {
                        **base_metadata,
                        'chunk_id': f"{file_path.stem}_para_{i+1}",
                        'chunk_type': 'paragraph',
                        'paragraph_index': i + 1,
                        'file_path': str(file_path.relative_to(file_path.parent.parent))
                    }
                })

        return chunks

    def _chunk_by_sentence(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """句子级别分块 - 按句子分割"""
        # 提取基本元数据
        base_metadata = self._extract_metadata(content, file_path)

        # 简单的句子分割（针对中文优化）
        sentences = re.split(r'[。！？\n]\s*', content.strip())
        chunks = []

        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if sentence and len(sentence) > 10:  # 忽略太短的句子
                chunks.append({
                    'content': sentence,
                    'metadata': {
                        **base_metadata,
                        'chunk_id': f"{file_path.stem}_sent_{i+1}",
                        'chunk_type': 'sentence',
                        'sentence_index': i + 1,
                        'file_path': str(file_path.relative_to(file_path.parent.parent))
                    }
                })

        return chunks

    def _extract_metadata(self, content: str, file_path: Path) -> Dict[str, Any]:
        """从文档内容中提取元数据"""
        metadata = {
            'filename': file_path.name,
            'file_type': file_path.suffix.lower(),
            'file_size': len(content),
        }

        # 如果是markdown文件，提取标题
        if file_path.suffix.lower() == '.md':
            # 提取一级标题
            h1_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if h1_match:
                metadata['title'] = h1_match.group(1).strip()

            # 提取第一个二级标题作为摘要
            h2_match = re.search(r'^## (.+)$', content, re.MULTILINE)
            if h2_match:
                metadata['first_section'] = h2_match.group(1).strip()

        return metadata