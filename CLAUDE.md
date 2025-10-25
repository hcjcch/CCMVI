# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 Android 开发知识库项目，包含三个主要部分：

1. **Android MVI 架构文档库** (`core/`, `components/`) - 基于 Compose + ViewModel 的 MVI 架构规范
2. **RAG 检索系统** (`android-knowledge-rag/`) - Python 实现的知识检索增强生成系统
3. **MCP 服务器** (`android-knowledge-mcp/`) - Model Context Protocol 服务器，提供智能知识检索工具

## 常用命令

### 环境管理（优先执行）
```bash
# 检查并创建虚拟环境（RAG 系统）
cd android-knowledge-rag/
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# 检查并创建虚拟环境（MCP 服务器）
cd android-knowledge-mcp/
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### RAG 系统命令
```bash
# 进入 RAG 系统目录
cd android-knowledge-rag/

# 激活 Python 虚拟环境
source venv/bin/activate  # Linux/Mac

# 构建知识库索引
python src/cli.py build --granularity paragraph

# 搜索知识
python src/cli.py search "MVI架构"

# 重置数据库并重新构建
python src/cli.py build --reset

# 或使用便捷脚本
./knowledge-search "MVI架构"
```

### MCP 服务器命令
```bash
# 进入 MCP 服务器目录
cd android-knowledge-mcp/

# 激活 Python 虚拟环境
source venv/bin/activate  # Linux/Mac

# 启动 MCP 服务器
python run_server.py

# 或直接运行主文件
python src/mcp_server.py
```

### Claude Code MCP 集成配置
```json
{
  "mcpServers": {
    "android-knowledge": {
      "command": "python",
      "args": ["/absolute/path/to/android-knowledge-mcp/run_server.py"],
      "cwd": "/absolute/path/to/android-knowledge-mcp/"
    }
  }
}
```

## 核心架构

### MVI（Model-View-Intent）架构
本项目采用单向数据流架构，关键原则：

- **数据驱动**：界面由数据状态变化驱动 UI 更新
- **边界清晰**：各层职责明确，避免逻辑混杂
- **单向数据流**：数据从 Repository → ViewModel → Screen/View
- **单向事件流**：事件通过回调形式从 View → Screen → ViewModel

### MCP 工具架构
MCP 服务器提供以下核心工具：
- **search_core_architecture**: 查询 MVI 架构和 Kotlin 编码规范
- **search_component_guide**: 查询特定组件（ViewModel、Activity、LiveData 等）使用指南
- **search_knowledge**: 通用知识搜索，支持细粒度过滤

### 三层知识检索系统
1. **文档库层** (`core/`, `components/`) - 结构化的架构和组件规范
2. **RAG 检索层** (`android-knowledge-rag/`) - 基于向量搜索的语义检索
3. **MCP 服务层** (`android-knowledge-mcp/`) - 标准化的智能工具接口

### 文件命名规范
- `{Name}ViewModel`: 管理数据状态，持有 LiveData
- `{Name}Repository`: 数据源，负责网络和本地数据获取
- `{Name}Activity`: 界面入口，Android 四大组件之一
- `{Name}Screen`: Compose 入口函数，组合各种 View
- `{Name}View`: 构成 UI 的小组合函数
- `{Name}Utils`: 工具类，包含 Kotlin 顶级函数
- `{Name}UiState`: UI 状态类，驱动 View 渲染

### 各层职责

**Activity 层**：
- 处理页面跳转协议
- 初始化 ViewModel
- 加载对应的 Entry Screen

**ViewModel 层**：
- 作为数据源的唯一持有者
- 从 Repository 获取数据
- 持有 LiveData 传输数据

**Screen 层**：
- 组装子 View 组件
- 通过 ViewModel 中转事件
- 分发数据给子组件

**View 层**：
- 渲染 UI 界面
- 定义用户交互事件
- 保持纯函数特性

## 编码规范

### Kotlin 代码规则
- **import**: 必须全量引入，不能使用 `import *`
- **类型定义**:
  - String 等对象类型必须声明为可空类型，初始化为 null
  - 简单类型声明为非空类型，并初始化
- **注释**:
  - 类成员变量、函数、类使用多行注释 `/** */`
  - 变量使用单行注释 `//`

### 设计原则
- 函数单一职责
- 类单一职责
- 文件内容规则：一个文件只能有一个主类和多个内部类

## 技术栈和依赖

### RAG 检索系统
- `chromadb>=0.4.0`: 向量数据库，用于存储和检索文档嵌入
- `sentence-transformers>=2.2.0`: 句子嵌入模型，用于语义搜索
- `click>=8.1.0`: 命令行接口框架
- `rich>=13.0.0`: 终端输出美化
- `python-dotenv>=1.0.0`: 环境变量管理
- `markdown>=3.4.0`: Markdown 文档解析

### MCP 服务器
- `mcp>=1.0.0`: Model Context Protocol 核心库
- 复用 RAG 系统的所有依赖
- `pathlib2>=2.3.0`: 路径操作增强
- `typing-extensions>=4.0.0`: 类型注解扩展

### 支持的文档分块粒度
- `file`: 按文件分块 - 适合查找完整规范
- `paragraph`: 按段落分块 - 平衡精度和上下文（推荐）
- `sentence`: 按句子分块 - 适合精确查询

### MCP 工具使用场景
- **智能编码指导**: 自动调用获取架构规范
- **组件使用查询**: 特定组件的最佳实践
- **深度知识搜索**: 全面的架构和编码知识检索

## 项目结构

```
.
├── core/                           # 核心架构文档
│   ├── Architecture.md             # MVI 架构规范
│   └── KotlinCodeRules.md          # Kotlin 编码规范
├── components/                     # 组件规范文档
│   ├── Activity.md                 # Activity 组件规范
│   ├── ViewModel.md                # ViewModel 组件规范
│   ├── LiveData.md                 # LiveData 组件规范
│   ├── KotlinFlow.md               # Kotlin Flow 组件规范
│   └── UI.md                       # UI 组件规范
├── android-knowledge-rag/          # RAG 知识检索系统
│   ├── src/                        # Python 源代码
│   │   ├── cli.py                 # 命令行工具
│   │   ├── config.py              # 配置管理
│   │   ├── document_processor.py  # 文档处理
│   │   └── vector_store.py        # 向量存储
│   ├── knowledge-search            # 可执行搜索脚本
│   ├── data/                       # 数据目录
│   ├── requirements.txt            # Python 依赖
│   └── venv/                       # Python 虚拟环境
└── android-knowledge-mcp/          # MCP 服务器实现
    ├── src/
    │   └── mcp_server.py          # MCP 服务器主文件
    ├── run_server.py              # 启动脚本
    ├── requirements.txt           # MCP 依赖
    ├── USAGE_EXAMPLES.md          # 使用示例
    ├── MCP_接入文档.md             # MCP 接入文档
    └── venv/                      # Python 虚拟环境
```

## 开发工作流程

### 1. 环境初始化（首次使用）
```bash
# 1. 设置 RAG 系统
cd android-knowledge-rag/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/cli.py build --granularity paragraph

# 2. 设置 MCP 服务器
cd ../android-knowledge-mcp/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 配置 Claude Code（在 Claude Code 配置中添加 MCP 服务器）
# 参考上文的 Claude Code MCP 集成配置
```

### 2. 日常开发流程
```bash
# 启动 MCP 服务器（用于 Claude Code 智能检索）
cd android-knowledge-mcp/
source venv/bin/activate
python run_server.py

# 直接搜索知识（独立使用）
cd android-knowledge-rag/
source venv/bin/activate
./knowledge-search "你的查询内容"
```

### 3. 知识库维护
```bash
# 当更新文档后，重建索引
cd android-knowledge-rag/
source venv/bin/activate
python src/cli.py build --reset

# 检索最新知识
python src/cli.py search "新的架构概念"
```

## 开发建议和最佳实践

### 架构遵循
1. **严格遵循 MVI 架构**：单向数据流，职责分离
2. **保持代码规范**：按照 KotlinCodeRules.md 进行编码
3. **组件职责明确**：每个组件只负责自己的职责范围
4. **状态管理集中**：所有状态数据通过 ViewModel 集中管理

### 智能开发
1. **启用 MCP 集成**：让 Claude Code 自动调用知识库工具
2. **善用语义搜索**：通过 knowledge-search 快速查找相关知识
3. **遵循最佳实践**：基于检索到的架构指导进行开发
4. **持续学习**：利用知识库深入理解 MVI 架构细节

### 文档维护
1. **及时更新规范**：架构演进时同步更新文档
2. **重建知识索引**：文档更新后重新构建 RAG 索引
3. **验证检索质量**：定期测试搜索结果的准确性

## 故障排除

### 常见问题
- **MCP 连接失败**：检查 Python 路径和虚拟环境配置
- **搜索无结果**：确认知识库索引已构建，使用 `build --reset` 重建
- **依赖安装失败**：确保 Python 版本兼容，使用虚拟环境
- **路径问题**：使用绝对路径配置 MCP 服务器