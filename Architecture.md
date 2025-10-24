# Compose + ViewModel 单项数据流开发架构知识库
## 文件命名
- **{Name}ViewModel**: 负责管理数据状态[ViewModel 链接](ViewModel.md)，持有 LiveData
- **{Name}Repository**: 数据来源，负责网络数据和本地数据获取
- **{Name}Activity**: 一个界面的入口，Android 四大组件中的 Activity，持有 ViewModel，chu'shi
- **{Name}Screen**: 一个 Compose 函数，Activity 设置界面时调用的入口函数，里面组合着各种 View
- **{Name}View**: 被 Screen 组合，是构成用户界面的一个个小组合(Compose)函数
- **{Name}Utils**: 工具类，里面都是 Kotlin 顶级函数
- **{Name}UiState**: UI 的状态类，这个 UIState 驱动 View 的渲染

## 架构目标
- **数据驱动**：界面由数据状态变化驱动 UI 更新
- **边界清晰**：各层职责明确，避免逻辑混杂
- **单向数据流**：数据只能从源头单向流动，避免共享数据导致的时序问题
- **单项事件流**: 事件只能从 View 传到 Screen，最终调用 ViewModel 改变源数据，事件采用回调的形式

## 核心分层结构

### Activity 层
**职责**：
- 处理页面跳转协议
- 初始化 ViewModel
- 加载对应的 Entry Screen

**原则**：
- 仅作为界面载体，不包含业务逻辑
- 一个 Activity 对应一个 Entry Screen

### ViewModel 层
**职责**：
- 作为数据源的唯一持有者
- 数据从 Repository 获取
- 持有 LiveData，LiveData 给 Screen 传输数据，数据最终给到 Screen 以及 Screen 的子 View

**原则**：
- 管理页面级状态数据
- 处理业务逻辑和异步操作

### Entry Screen（入口可组合函数）
**职责**：
- 组装子 View 组件
- 通过 ViewModel 中转事件
- 分发数据给子组件

**原则**：
- 使用 `@Composable` 函数实现，因为它是一个可组合函数
- 接收 ViewModel 作为参数
- 不处理具体业务逻辑

### View（非入口可组合函数）
**职责**：
- 渲染 UI 界面
- 定义用户交互事件

**原则**：
- 构造参数不能是 ViewModel
- 数据仅从参数获取，通过 listener 传递事件
- 保持纯函数特性（快速、幂等、无副作用）

## 关键设计原则

### 单向数据流
- Repository 产生数据，经 ViewModel 的 LiveData 传到 Screen 和 View
### 单向事件流
- View 产生事件，事件经传入的高阶回调函数传到 Screen，调用 ViewModel 的函数处理事件，更新数据源
