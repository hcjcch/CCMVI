# Android 知识库 MCP 服务器接入文档

## 概述

本文档介绍如何配置和使用 Android 知识库 MCP (Model Context Protocol) 服务器，该服务器为 JoyCode Agent 提供智能的 Android 架构规范和编码指导。

## 服务器信息

- **服务名称**: `android-knowledge-rag`
- **服务类型**: MCP 服务器
- **协议**: stdio 传输
- **功能**: Android 开发知识检索与架构规范查询

## 核心功能

### 1. 核心架构查询
- **工具名**: `search_core_architecture`
- **用途**: 获取 MVI 架构规范和 Kotlin 编码规则
- **调用时机**: 每次 Android 编码任务开始时自动调用
- **参数**: 无需参数
- **返回内容**:
  - MVI 架构原则和设计规范
  - Kotlin 编码规则和最佳实践
  - 文件命名规范
  - 各层职责定义

### 2. 组件指南查询
- **工具名**: `search_component_guide`
- **用途**: 查询特定 Android 组件的详细使用指南
- **参数**:
  - `component_type` (必需): 组件类型
    - `"ViewModel"`: 数据管理和状态控制
    - `"Activity"`: 界面入口和生命周期
    - `"LiveData"`: 响应式数据观察
    - `"KotlinFlow"`: 异步数据流
    - `"UI"`: 界面组件和交互
  - `query` (可选): 具体查询内容，如"状态管理"、"生命周期"等

### 3. 通用知识搜索
- **工具名**: `search_knowledge`
- **用途**: 基于语义相似度的 Android 知识检索
- **参数**:
  - `query` (必需): 搜索关键词或问题
  - `top_k` (可选): 返回结果数量，范围 1-10，默认 5
  - `filter_type` (可选): 过滤类型
    - `"core"`: 仅搜索核心架构文档
    - `"components"`: 仅搜索组件规范文档
    - `"all"`: 搜索所有文档（默认）

## 接入配置

### 步骤 1: 环境准备

1. **确认 Python 虚拟环境**:
   ```bash
   cd /Users/huangchen/Develop/mvi/lib/knowledge/android-knowledge-mcp
   source venv/bin/activate
   ```

2. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

3. **测试服务**:
   ```bash
   python test_mcp_service.py
   ```

### 步骤 2: 配置 MCP 客户端

在您的 MCP 客户端配置文件中添加以下配置：

#### 配置文件位置
- **Claude Code**: `~/.claude/settings.json` 或相关配置文件
- **其他客户端**: 根据具体客户端确定配置文件位置

#### 配置内容
```json
{
  "mcpServers": {
    "android-knowledge-rag": {
      "command": "python",
      "args": ["/Users/huangchen/Develop/mvi/lib/knowledge/android-knowledge-mcp/run_server.py"],
      "disabled": false,
      "alwaysAllow": [
        "search_core_architecture",
        "search_component_guide",
        "search_knowledge"
      ],
      "env": {
        "PYTHONPATH": "/Users/huangchen/Develop/mvi/lib/knowledge/android-knowledge-rag/src"
      }
    }
  }
}
```

### 步骤 3: 重启客户端

配置完成后，重启您的 MCP 客户端以加载新的服务器配置。

## 使用指南

### 自动调用场景

MCP 服务器设计为在以下场景自动被 JoyCode Agent 调用：

1. **任务初始化**: 当检测到 Android 编码任务时，自动调用 `search_core_architecture` 获取基础架构规范
2. **组件开发**: 识别到特定组件开发时，调用 `search_component_guide` 获取组件指导
3. **深度查询**: 需要特定知识时，调用 `search_knowledge` 进行语义搜索

### 手动调用示例

#### 查询核心架构规范
```python
# 通过 MCP 客户端调用
result = mcp_execute_tool(
    "android-knowledge-rag",
    "search_core_architecture",
    {}
)
```

#### 查询 ViewModel 使用指南
```python
result = mcp_execute_tool(
    "android-knowledge-rag",
    "search_component_guide",
    {
        "component_type": "ViewModel",
        "query": "状态管理最佳实践"
    }
)
```

#### 搜索特定知识
```python
result = mcp_execute_tool(
    "android-knowledge-rag",
    "search_knowledge",
    {
        "query": "LiveData 和 Flow 的区别",
        "top_k": 3,
        "filter_type": "components"
    }
)
```

## 技术架构

### 系统组件
- **MCP 服务器**: 基于 `mcp>=1.0.0` 实现
- **向量存储**: 集成现有的 ChromaDB
- **知识缓存**: 核心架构文档预加载到内存
- **RAG 系统**: 复用 `android-knowledge-rag` 系统的向量搜索能力

### 数据源
- **核心架构文档**: `core/Architecture.md`, `core/KotlinCodeRules.md`
- **组件规范**: `components/` 目录下的各组件文档
- **向量数据库**: `android-knowledge-rag/data/chroma_db/`

### 性能优化
- **缓存策略**: 核心知识内存缓存，毫秒级响应
- **智能路由**: 根据查询类型选择最优检索策略
- **异步处理**: 使用 asyncio 提升并发性能

## 故障排除

### 常见问题

#### 1. 服务器启动失败
**症状**: MCP 客户端无法连接到服务器
**解决方案**:
```bash
# 检查 Python 环境
cd /Users/huangchen/Develop/mvi/lib/knowledge/android-knowledge-mcp
source venv/bin/activate
python src/mcp_server.py

# 检查依赖
pip install -r requirements.txt
```

#### 2. 向量数据库未初始化
**症状**: 搜索功能返回空结果
**解决方案**:
```bash
cd /Users/huangchen/Develop/mvi/lib/knowledge/android-knowledge-rag
source venv/bin/activate
python src/cli.py build --granularity paragraph
```

#### 3. 导入错误
**症状**: 服务器启动时出现模块导入错误
**解决方案**:
```bash
# 确保 PYTHONPATH 正确设置
export PYTHONPATH="/Users/huangchen/Develop/mvi/lib/knowledge/android-knowledge-rag/src:$PYTHONPATH"
```

#### 4. 权限问题
**症状**: 启动脚本无法执行
**解决方案**:
```bash
chmod +x /Users/huangchen/Develop/mvi/lib/knowledge/android-knowledge-mcp/run_server.py
```

### 调试模式

启用详细日志进行调试：

```bash
# 设置环境变量启用调试
export MCP_DEBUG=1
export PYTHONPATH="/Users/huangchen/Develop/mvi/lib/knowledge/android-knowledge-rag/src"

# 运行服务器
python src/mcp_server.py
```

## 测试验证

### 功能测试
```bash
# 运行完整测试套件
cd /Users/huangchen/Develop/mvi/lib/knowledge/android-knowledge-mcp
python test_mcp_service.py
```

### 连接测试
在 MCP 客户端中执行以下测试：

1. **列出可用工具**:
   ```python
   tools = mcp_list_tools("android-knowledge-rag")
   ```

2. **测试核心查询**:
   ```python
   result = mcp_execute_tool("android-knowledge-rag", "search_core_architecture", {})
   ```

3. **验证搜索功能**:
   ```python
   result = mcp_execute_tool("android-knowledge-rag", "search_knowledge", {
       "query": "Android MVI 架构"
   })
   ```

## 维护和更新

### 添加新知识
1. 在 `core/` 或 `components/` 目录添加新文档
2. 更新向量数据库：
   ```bash
   cd android-knowledge-rag
   python src/cli.py build --granularity paragraph
   ```
3. 重启 MCP 服务器

### 扩展工具功能
1. 编辑 `src/mcp_server.py` 中的 `setup_handlers()` 方法
2. 添加新的工具定义和处理函数
3. 更新测试脚本

### 版本更新
```bash
cd /Users/huangchen/Develop/mvi/lib/knowledge/android-knowledge-mcp
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

## 最佳实践

### 1. 自动化工作流
- 在每次 Android 编码任务开始时自动调用核心架构查询
- 根据代码上下文自动选择合适的组件指南

### 2. 查询优化
- 使用具体的查询关键词获得更精确的结果
- 合理设置 `top_k` 参数平衡性能和完整性

### 3. 知识管理
- 定期更新架构文档和组件规范
- 保持向量数据库与文档同步

## 支持和反馈

如果遇到问题或需要功能扩展，请：

1. 检查本文档的故障排除部分
2. 运行测试脚本诊断问题
3. 查看服务器日志了解详细错误信息

---

*本文档持续更新，以保持与 MCP 服务器功能同步。*