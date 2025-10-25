# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 Android 开发知识库项目，包含两个主要部分：

1. **Android MVI 架构文档库** (`core/`, `components/`) - 基于 Compose + ViewModel 的 MVI 架构规范
2. **RAG 检索系统** (`android-knowledge-rag/`) - Python 实现的知识检索增强生成系统

## 常用命令

### RAG 系统命令
```bash
# 进入 RAG 系统目录
cd android-knowledge-rag/

# 激活 Python 虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 构建知识库索引
python src/cli.py build --granularity paragraph

# 搜索知识
python src/cli.py search "MVI架构"

# 重置数据库并重新构建
python src/cli.py build --reset
```

### 开发环境设置
```bash
# 创建 Python 虚拟环境（如果不存在）
python -m venv venv

# 安装开发依赖
pip install -r requirements.txt
```

## 核心架构

### MVI（Model-View-Intent）架构
本项目采用单向数据流架构，关键原则：

- **数据驱动**：界面由数据状态变化驱动 UI 更新
- **边界清晰**：各层职责明确，避免逻辑混杂
- **单向数据流**：数据从 Repository → ViewModel → Screen/View
- **单向事件流**：事件通过回调形式从 View → Screen → ViewModel

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

## RAG 系统组件

### 核心依赖
- `chromadb>=0.4.0`: 向量数据库
- `sentence-transformers>=2.2.0`: 句子嵌入模型
- `click>=8.1.0`: 命令行接口
- `rich>=13.0.0`: 美化终端输出

### 支持的文档分块粒度
- `file`: 按文件分块
- `paragraph`: 按段落分块
- `sentence`: 按句子分块

### 使用场景
- 快速检索 Android 开发相关的架构知识
- 查找编码规范和最佳实践
- 理解 MVI 架构的实现细节

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
└── android-knowledge-rag/          # RAG 系统实现
    ├── src/                        # Python 源代码
    ├── data/                       # 数据文件
    ├── requirements.txt            # Python 依赖
    └── venv/                       # Python 虚拟环境
```

## 开发建议

1. **遵循架构原则**：严格遵循 MVI 单向数据流模式
2. **保持代码规范**：按照 KotlinCodeRules.md 进行编码
3. **使用 RAG 系统**：利用 knowledge-search 工具快速查找知识
4. **组件职责明确**：确保每个组件只负责自己的职责范围
5. **状态管理集中**：所有状态数据通过 ViewModel 集中管理