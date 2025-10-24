# Android 开发知识库

这是一个基于 Android Compose + ViewModel MVI 架构的知识库项目，同时包含 RAG（检索增强生成）系统的实现。

## 项目结构

```
.
├── core/                           # 核心架构和规则
│   ├── Architecture.md             # Compose + ViewModel MVI 架构文档
│   └── KotlinCodeRules.md          # Kotlin 编码规范
├── components/                     # 组件相关文档
│   ├── Activity.md                 # Activity 组件规范
│   ├── ViewModel.md                # ViewModel 组件规范
│   ├── LiveData.md                 # LiveData 组件规范
│   ├── KotlinFlow.md               # Kotlin Flow 组件规范
│   └── UI.md                       # UI 组件规范
└── android-knowledge-rag/          # RAG 系统实现
    ├── src/                        # 源代码
    ├── data/                       # 数据文件
    ├── scripts/                    # 脚本文件
    ├── tests/                      # 测试文件
    ├── requirements.txt            # Python 依赖
    └── venv/                       # Python 虚拟环境
```

## 核心架构

### MVI（Model-View-Intent）架构

本项目采用基于 Compose + ViewModel 的单向数据流架构：

- **数据驱动**：界面由数据状态变化驱动 UI 更新
- **边界清晰**：各层职责明确，避免逻辑混杂
- **单向数据流**：数据只能从源头单向流动
- **单向事件流**：事件通过回调形式向上传递

### 核心组件

#### Activity 层
- 处理页面跳转协议
- 初始化 ViewModel
- 加载对应的 Entry Screen

#### ViewModel 层
- 作为数据源的唯一持有者
- 从 Repository 获取数据
- 持有 LiveData 传输数据

#### Screen 层
- 组装子 View 组件
- 通过 ViewModel 中转事件
- 分发数据给子组件

#### View 层
- 渲染 UI 界面
- 定义用户交互事件
- 保持纯函数特性

## 文件命名规范

- **{Name}ViewModel**: 负责管理数据状态的 ViewModel
- **{Name}Repository**: 数据来源，负责网络和本地数据获取
- **{Name}Activity**: 界面入口，Android 四大组件之一
- **{Name}Screen**: Compose 入口函数，组合各种 View
- **{Name}View**: 构成用户界面的小组合函数
- **{Name}Utils**: 工具类，包含 Kotlin 顶级函数
- **{Name}UiState**: UI 状态类，驱动 View 渲染

## 编码规范

### 基本规则
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

## RAG 系统

`android-knowledge-rag/` 目录包含了一个完整的 RAG 系统实现：

- **Python 虚拟环境**: 使用独立的虚拟环境进行 Python 开发
- **知识检索**: 基于 Android 开发知识的智能检索系统
- **数据处理**: 包含数据清洗、向量化等处理流程

## 使用指南

### 查找知识
使用项目中的 `knowledge-search` 工具来快速查找相关的开发知识和编码规范。

### 遵循规范
在开发过程中，请务必遵循 `knowledge/core/` 目录下定义的架构和编码规范。

## 贡献指南

1. 新增知识内容时，请按照现有的文档结构进行组织
2. 编码时严格遵循 `KotlinCodeRules.md` 中定义的规范
3. 架构设计请参考 `Architecture.md` 中的指导原则

---

*本知识库旨在为 Android 开发提供统一的架构指导和编码规范，确保代码质量和开发效率。*