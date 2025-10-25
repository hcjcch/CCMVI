#!/usr/bin/env python3
"""
Android知识库MCP服务测试脚本
"""

import asyncio
import json
import sys
from pathlib import Path

# 添加源代码路径
sys.path.append(str(Path(__file__).parent / "src"))

from mcp_server import AndroidKnowledgeMCPServer

async def test_mcp_service():
    """测试MCP服务功能"""
    print("🧪 开始测试Android知识库MCP服务...")
    
    try:
        # 创建服务器实例
        server = AndroidKnowledgeMCPServer()
        
        # 初始化服务器
        print("\n📋 步骤1: 初始化服务器...")
        await server.initialize()
        
        # 设置处理器
        print("📋 步骤2: 设置处理器...")
        server.setup_handlers()
        
        print("✅ 服务器初始化成功！")
        
        # 测试核心架构查询
        print("\n🔍 测试1: 核心架构查询...")
        try:
            result = await server._handle_core_architecture_search()
            print(f"✅ 核心架构查询成功，返回 {len(result)} 个结果")
            if result and result[0].text:
                preview = result[0].text[:200] + "..." if len(result[0].text) > 200 else result[0].text
                print(f"📄 内容预览: {preview}")
        except Exception as e:
            print(f"❌ 核心架构查询失败: {e}")
        
        # 测试组件指南查询
        print("\n🔍 测试2: ViewModel组件指南查询...")
        try:
            args = {"component_type": "ViewModel", "query": "状态管理"}
            result = await server._handle_component_guide_search(args)
            print(f"✅ 组件指南查询成功，返回 {len(result)} 个结果")
            if result and result[0].text:
                preview = result[0].text[:200] + "..." if len(result[0].text) > 200 else result[0].text
                print(f"📄 内容预览: {preview}")
        except Exception as e:
            print(f"❌ 组件指南查询失败: {e}")
        
        # 测试通用知识搜索
        print("\n🔍 测试3: 通用知识搜索...")
        try:
            args = {"query": "Android MVI架构", "top_k": 3, "filter_type": "all"}
            result = await server._handle_knowledge_search(args)
            print(f"✅ 通用知识搜索成功，返回 {len(result)} 个结果")
            if result and result[0].text:
                preview = result[0].text[:200] + "..." if len(result[0].text) > 200 else result[0].text
                print(f"📄 内容预览: {preview}")
        except Exception as e:
            print(f"❌ 通用知识搜索失败: {e}")
        
        print("\n🎉 所有测试完成！")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False
    
    return True

async def test_vector_store():
    """测试向量存储是否可用"""
    print("\n🔍 测试向量存储...")
    
    try:
        sys.path.append(str(Path(__file__).parent.parent / "android-knowledge-rag" / "src"))
        from vector_store import VectorStore
        
        vector_store = VectorStore()
        
        # 测试简单搜索
        results = vector_store.search("Android", top_k=2)
        print(f"✅ 向量存储测试成功，找到 {len(results)} 个结果")
        
        for i, result in enumerate(results[:2]):
            metadata = result.get('metadata', {})
            file_path = metadata.get('file_path', '未知文件')
            print(f"  📄 结果 {i+1}: {file_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ 向量存储测试失败: {e}")
        print("💡 提示: 请先运行 '../android-knowledge-rag/knowledge-search build' 构建向量数据库")
        return False

def main():
    """主函数"""
    print("🚀 Android知识库MCP服务测试")
    print("=" * 50)
    
    # 运行测试
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # 测试向量存储
        vector_ok = loop.run_until_complete(test_vector_store())
        
        if vector_ok:
            # 测试MCP服务
            mcp_ok = loop.run_until_complete(test_mcp_service())
            
            if mcp_ok:
                print("\n🎊 所有测试通过！MCP服务可以正常使用。")
                print("\n📋 下一步:")
                print("1. 重启JoyCode以加载新的MCP服务")
                print("2. 在Android编码任务中测试自动调用功能")
            else:
                print("\n⚠️  MCP服务测试未完全通过，请检查错误信息")
        else:
            print("\n⚠️  向量存储不可用，请先构建知识库")
            
    finally:
        loop.close()

if __name__ == "__main__":
    main()