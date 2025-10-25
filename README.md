# Android 开发知识库

基于 Compose + ViewModel 的 MVI 架构规范与 MCP (Model Context Protocol) 集成。

## 项目结构

```
├── core/                    # 核心架构文档
│   ├── Architecture.md     # MVI 架构规范
│   └── KotlinCodeRules.md  # Kotlin 编码规范
├── components/             # 组件规范文档
├── mcp/                    # MCP 服务器实现
└── knowledge-search        # 知识搜索命令行工具
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
cd mcp/
python server.py

# 在 Claude Code 中使用 MCP 工具
# - 搜索架构知识
# - 获取编码规范
# - 查询最佳实践
```

### 依赖

- `mcp>=1.0.0`: Model Context Protocol 核心库
- `chromadb>=0.4.0`: 向量数据库
- `sentence-transformers>=2.2.0`: 句子嵌入模型

## 使用指南

1. **架构设计**: 遵循 `core/Architecture.md` 中的 MVI 架构原则
2. **编码规范**: 按照 `core/KotlinCodeRules.md` 编写代码
3. **智能辅助**: 使用 MCP 工具实时获取架构指导和编码建议

---

*统一的 Android 架构指导和编码规范，确保代码质量和开发效率*