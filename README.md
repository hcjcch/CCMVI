# Android 开发知识库

基于 Compose + ViewModel 的 MVI 架构规范与 MCP (Model Context Protocol) 集成。

## 项目结构

```
├── core/                           # 核心架构文档
│   ├── Architecture.md           # MVI 架构规范
│   └── KotlinCodeRules.md        # Kotlin 编码规范
├── components/                     # 组件规范文档
│   ├── Activity.md                 # Activity 组件规范
│   ├── ViewModel.md                # ViewModel 组件规范
│   ├── LiveData.md                 # LiveData 组件规范
│   ├── KotlinFlow.md               # Kotlin Flow 组件规范
│   └── UI.md                       # UI 组件规范
├── android-knowledge-mcp/           # MCP 服务器实现
└── android-knowledge-rag/           # 知识检索系统
    ├── knowledge-search            # 知识搜索命令行工具
    ├── src/                        # Python 源代码
    └── requirements.txt            # Python 依赖
```

## MVI 架构核心

- **单向数据流**: Repository → ViewModel → Screen → View
- **数据驱动**: UI 由数据状态变化驱动
- **职责清晰**: 各层组件职责明确，边界清晰

### 组件职责

| 层级 | 组件 | 职责 |
|------|------|------|
| Activity | {Name}Activity | 页面跳转、初始化 ViewModel |
| ViewModel | {Name}ViewModel | 数据状态管理、LiveData 持有 |
| Screen | {Name}Screen | 组装子组件、事件中转 |
| View | {Name}View | UI 渲染、交互事件定义 |
| Data | {Name}Repository | 数据获取（网络/本地） |

## 编码规范

- **import**: 必须全量引入，禁用 `import *`
- **类型定义**: 对象类型声明为可空并初始化为 null，简单类型声明为非空
- **注释**: 类/函数用 `/** */`，变量用 `//`
- **职责**: 函数和类都遵循单一职责原则

## MCP 集成

### MCP 服务器功能

- **智能搜索**: 基于 Android 架构知识的语义搜索
- **代码规范**: 实时提供 MVI 架构和 Kotlin 编码规范
- **最佳实践**: 返回符合项目标准的实现建议

### 快速开始

```bash
# 启动 MCP 服务器
cd android-knowledge-mcp/
python run_server.py

# 使用知识检索系统
cd android-knowledge-rag/
./knowledge-search "MVI架构"

# 在 Claude Code 中使用 MCP 工具
# - 搜索架构知识
# - 获取编码规范
# - 查询最佳实践
```

### 依赖

- `mcp>=1.0.0`: Model Context Protocol 核心库
- `chromadb>=0.4.0`: 向量数据库
- `sentence-transformers>=2.2.0`: 句子嵌入模型

## MCP 集成指南

### 1. 环境准备

```bash
# 进入 MCP 服务器目录
cd android-knowledge-mcp/

# 创建并激活 Python 虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 Claude Code

在 Claude Code 配置文件中添加 MCP 服务器：

```json
{
  "mcpServers": {
    "android-knowledge": {
      "command": "python",
      "args": ["/path/to/android-knowledge-mcp/run_server.py"],
      "cwd": "/path/to/android-knowledge-mcp/"
    }
  }
}
```

### 3. 启动服务

```bash
# 方式 1: 直接启动 MCP 服务器
python run_server.py

# 方式 2: 通过 Claude Code 自动启动
# 重启 Claude Code，MCP 服务器将自动连接
```

### 4. 使用 MCP 工具

在 Claude Code 中可直接使用以下工具：

- `android_knowledge_search`: 搜索 Android 架构知识
- `get_coding_standards`: 获取 Kotlin 编码规范
- `architecture_guidance`: 获取 MVI 架构指导

### 5. 故障排除

- **连接失败**: 检查 Python 路径和虚拟环境是否正确
- **权限问题**: 确保 MCP 服务器文件有执行权限
- **端口冲突**: 修改服务器配置中的端口号

---

*统一的 Android 架构指导和编码规范，确保代码质量和开发效率*