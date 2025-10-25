#!/usr/bin/env python3
"""
Android知识库MCP服务器
为Android编码任务提供智能知识检索服务
"""

import sys
import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

# MCP SDK imports
from mcp import ClientSession, ServerSession
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# 导入现有RAG系统
sys.path.append(str(Path(__file__).parent.parent.parent / "android-knowledge-rag" / "src"))
from vector_store import VectorStore
from config import KNOWLEDGE_DIR

class AndroidKnowledgeMCPServer:
    """Android知识库MCP服务器"""
    
    def __init__(self):
        self.server = Server("android-knowledge-rag")
        self.vector_store: Optional[VectorStore] = None
        self.core_knowledge_cache: Dict[str, str] = {}
        
    async def initialize(self):
        """初始化服务器和RAG系统"""
        try:
            # 初始化向量存储
            self.vector_store = VectorStore()
            
            # 预加载核心架构知识
            await self._preload_core_knowledge()
            
            print("✅ Android知识库MCP服务器初始化成功", file=sys.stderr)
            
        except Exception as e:
            print(f"❌ 服务器初始化失败: {e}", file=sys.stderr)
            raise
    
    async def _preload_core_knowledge(self):
        """预加载核心架构知识到缓存"""
        core_files = [
            "core/Architecture.md",
            "core/KotlinCodeRules.md"
        ]
        
        for file_path in core_files:
            try:
                full_path = Path(__file__).parent.parent.parent / file_path
                if full_path.exists():
                    content = full_path.read_text(encoding='utf-8')
                    self.core_knowledge_cache[file_path] = content
                    print(f"✅ 已缓存核心知识: {file_path}", file=sys.stderr)
            except Exception as e:
                print(f"❌ 缓存失败 {file_path}: {e}", file=sys.stderr)
    
    def setup_handlers(self):
        """设置MCP处理器"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """列出可用工具"""
            return [
                types.Tool(
                    name="search_core_architecture",
                    description="查询Android核心架构规范和Kotlin编码规则（每次Android编码必查）",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                ),
                types.Tool(
                    name="search_component_guide",
                    description="查询特定Android组件的详细使用指南",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "component_type": {
                                "type": "string",
                                "enum": ["ViewModel", "Activity", "LiveData", "KotlinFlow", "UI"],
                                "description": "组件类型"
                            },
                            "query": {
                                "type": "string",
                                "description": "具体查询内容（可选）"
                            }
                        },
                        "required": ["component_type"],
                        "additionalProperties": False
                    }
                ),
                types.Tool(
                    name="search_knowledge",
                    description="通用Android知识搜索，基于语义相似度检索",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "搜索关键词或问题"
                            },
                            "top_k": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 10,
                                "default": 5,
                                "description": "返回结果数量"
                            },
                            "filter_type": {
                                "type": "string",
                                "enum": ["core", "components", "all"],
                                "default": "all",
                                "description": "过滤类型"
                            }
                        },
                        "required": ["query"],
                        "additionalProperties": False
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
            """处理工具调用"""
            try:
                if name == "search_core_architecture":
                    return await self._handle_core_architecture_search()
                elif name == "search_component_guide":
                    return await self._handle_component_guide_search(arguments)
                elif name == "search_knowledge":
                    return await self._handle_knowledge_search(arguments)
                else:
                    raise ValueError(f"未知工具: {name}")
                    
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"工具调用失败: {str(e)}"
                )]
    
    async def _handle_core_architecture_search(self) -> list[types.TextContent]:
        """处理核心架构查询"""
        result_parts = []
        
        # 从缓存获取核心知识
        for file_path, content in self.core_knowledge_cache.items():
            result_parts.append(f"## {file_path}\n\n{content}\n\n")
        
        if not result_parts:
            result_parts.append("⚠️ 核心架构知识未找到，请检查文件是否存在")
        
        return [types.TextContent(
            type="text", 
            text="".join(result_parts)
        )]
    
    async def _handle_component_guide_search(self, arguments: dict) -> list[types.TextContent]:
        """处理组件指南查询"""
        component_type = arguments["component_type"]
        query = arguments.get("query", "")
        
        # 构建组件文件路径
        component_file = f"components/{component_type}.md"
        
        try:
            # 直接读取组件文件
            file_path = Path(__file__).parent.parent.parent / component_file
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8')
                
                # 如果有具体查询，使用RAG搜索相关部分
                if query and self.vector_store:
                    search_query = f"{component_type} {query}"
                    search_results = self.vector_store.search(
                        search_query, 
                        top_k=3,
                        where={"file_path": {"$regex": f".*{component_type}.*"}}
                    )
                    
                    if search_results:
                        relevant_content = "\n\n".join([
                            f"### 相关内容 {i+1}\n{result['content']}" 
                            for i, result in enumerate(search_results)
                        ])
                        content = f"{content}\n\n## 相关搜索结果\n\n{relevant_content}"
                
                return [types.TextContent(
                    type="text",
                    text=f"## {component_type} 组件指南\n\n{content}"
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text=f"❌ 组件指南文件未找到: {component_file}"
                )]
                
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"❌ 查询组件指南失败: {str(e)}"
            )]
    
    async def _handle_knowledge_search(self, arguments: dict) -> list[types.TextContent]:
        """处理通用知识搜索"""
        query = arguments["query"]
        top_k = arguments.get("top_k", 5)
        filter_type = arguments.get("filter_type", "all")
        
        if not self.vector_store:
            return [types.TextContent(
                type="text",
                text="❌ 向量存储未初始化"
            )]
        
        try:
            # 构建过滤条件
            where_condition = None
            if filter_type == "core":
                where_condition = {"file_path": {"$regex": ".*core.*"}}
            elif filter_type == "components":
                where_condition = {"file_path": {"$regex": ".*components.*"}}
            
            # 执行搜索
            search_results = self.vector_store.search(
                query, 
                top_k=top_k,
                where=where_condition
            )
            
            if not search_results:
                return [types.TextContent(
                    type="text",
                    text=f"🔍 未找到与 '{query}' 相关的知识"
                )]
            
            # 格式化结果
            formatted_results = []
            for i, result in enumerate(search_results, 1):
                metadata = result.get('metadata', {})
                file_path = metadata.get('file_path', '未知文件')
                distance = result.get('distance', 0)
                
                formatted_results.append(
                    f"### 结果 {i} (相似度: {1-distance:.3f})\n"
                    f"**来源**: {file_path}\n\n"
                    f"{result['content']}\n"
                )
            
            return [types.TextContent(
                type="text",
                text=f"## 搜索结果: {query}\n\n" + "\n---\n\n".join(formatted_results)
            )]
            
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"❌ 知识搜索失败: {str(e)}"
            )]

async def main():
    """主函数"""
    # 创建MCP服务器实例
    mcp_server = AndroidKnowledgeMCPServer()
    
    # 初始化服务器
    await mcp_server.initialize()
    
    # 设置处理器
    mcp_server.setup_handlers()
    
    # 启动stdio服务器
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await mcp_server.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="android-knowledge-rag",
                server_version="1.0.0",
                capabilities=mcp_server.server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())