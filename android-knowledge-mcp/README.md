# Android知识库MCP服务

这是一个基于Model Context Protocol (MCP)的Android开发知识库服务，为JoyCode Agent提供智能的Android架构规范和编码指导。

## 🎯 功能特性

- **🏗️ 核心架构查询**: 自动提供MVI架构规范和Kotlin编码规则
- **🔧 组件指导**: 针对ViewModel、Activity、LiveData等组件的详细使用指南  
- **🔍 智能搜索**: 基于语义相似度的知识检索
- **⚡ 高性能**: 核心知识缓存，毫秒级响应
- **🔄 无缝集成**: 与现有RAG系统完美融合

## 📋 可用工具

### 1. `search_core_architecture`
- **用途**: 查询Android核心架构规范（每次编码必查）
- **参数**: 无需参数
- **返回**: MVI架构原则 + Kotlin编码规范

### 2. `search_component_guide`  
- **用途**: 查询特定组件使用指南
- **参数**: 
  - `component_type`: ViewModel | Activity | LiveData | KotlinFlow | UI
  - `query` (可选): 具体查询内容
- **返回**: 详细的组件使用指导

### 3. `search_knowledge`
- **用途**: 通用知识搜索
- **参数**:
  - `query`: 搜索关键词
  - `top_k`: 返回结果数量 (1-10, 默认5)
  - `filter_type`: core | components | all
- **返回**: 基于语义相似度的搜索结果

## 🚀 快速开始

### 1. 安装依赖

```bash
cd android-knowledge-mcp
source venv/bin/activate  # 激活虚拟环境
pip install -r requirements.txt
```

### 2. 启动服务

```bash
# 方式1: 使用启动脚本
./run_server.py

# 方式2: 直接运行
python src/mcp_server.py
```

### 3. 配置MCP客户端

将以下配置添加到JoyCode的MCP设置文件中：

```json
{
  "mcpServers": {
    "android-knowledge-rag": {
      "command": "python",
      "args": ["/path/to/android-knowledge-mcp/run_server.py"],
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

## 🏗️ 项目结构

```
android-knowledge-mcp/
├── src/
│   └── mcp_server.py          # MCP服务器主文件
├── venv/                      # Python虚拟环境
├── requirements.txt           # 项目依赖
├── run_server.py             # 启动脚本
└── README.md                 # 项目文档
```

## 🔧 技术架构

- **MCP协议**: 基于stdio传输的MCP服务器
- **RAG集成**: 复用现有的ChromaDB向量存储
- **缓存优化**: 核心架构知识预加载到内存
- **智能路由**: 根据查询类型自动选择最佳策略

## 🎯 使用场景

### 自动调用场景
当JoyCode Agent检测到Android编码任务时，会自动：

1. **任务开始** → 调用 `search_core_architecture` 获取基础规范
2. **组件识别** → 调用 `search_component_guide` 获取特定指导  
3. **深度查询** → 调用 `search_knowledge` 进行语义搜索

### 手动调用示例
```python
# 查询核心架构
mcp_execute_tool("android-knowledge-rag", "search_core_architecture", {})

# 查询ViewModel指南
mcp_execute_tool("android-knowledge-rag", "search_component_guide", {
    "component_type": "ViewModel",
    "query": "状态管理最佳实践"
})

# 通用知识搜索
mcp_execute_tool("android-knowledge-rag", "search_knowledge", {
    "query": "LiveData vs Flow 区别",
    "top_k": 3,
    "filter_type": "components"
})
```

## 🔍 故障排除

### 常见问题

1. **导入错误**: 确保RAG系统路径正确
2. **向量数据库未初始化**: 运行 `../android-knowledge-rag/knowledge-search build`
3. **权限问题**: 确保启动脚本有执行权限

### 调试模式

```bash
# 启用详细日志
PYTHONPATH=../android-knowledge-rag/src python src/mcp_server.py
```

## 📈 性能优化

- **核心知识缓存**: 避免重复文件读取
- **智能过滤**: 根据查询类型优化搜索范围
- **异步处理**: 使用asyncio提升并发性能

## 🔄 与现有系统集成

本MCP服务完全兼容现有的android-knowledge-rag系统：

- 共享相同的向量数据库
- 复用文档处理逻辑
- 保持配置一致性

## 📝 开发指南

### 添加新工具

1. 在 `setup_handlers()` 中添加工具定义
2. 实现对应的处理函数
3. 更新文档和测试

### 扩展知识源

1. 在现有RAG系统中添加新文档
2. 重新构建向量索引
3. MCP服务自动识别新内容

---

*本MCP服务让JoyCode Agent能够主动获取Android开发规范，确保生成的代码完全符合项目标准。*