# AI 编程指南：Android ViewModel

本文档旨在为你（AI 编程助手）提供在 Android 开发中使用 `ViewModel` 所需的核心上下文和最佳实践。

## 1. 核心概念：什么是 ViewModel？

`ViewModel` 是一个“业务逻辑”或“屏幕级状态容器”。它的核心职责有两个：

1.  **管理和缓存 UI 状态**：它持有 UI 所需的数据（例如，一个用户列表、表单的当前输入）。
2.  **封装业务逻辑**：它包含处理这些数据的逻辑（例如，从网络获取用户、验证表单）。

### 为什么使用 ViewModel？

`ViewModel` 的**最重要特性**是它能在“配置更改”（如屏幕旋转）后**存活**。

* **没有 ViewModel**：当用户旋转屏幕时，Activity 会被销毁并重建。Activity 中存储的所有 UI 状态（如网络请求的数据）都会丢失，需要重新获取。
* **使用 ViewModel**：`ViewModel` 的生命周期与创建它的 Activity/Fragment/Composable **分离**。当 Activity 重建时，它会收到**同一个** `ViewModel` 实例，数据依然存在，无需重新加载。

## 2. 如何实现 ViewModel

### 步骤 1：定义 ViewModel 类

创建一个继承 `androidx.lifecycle.ViewModel` 的类。

**关键实践**：
* 使用 `StateFlow` (Kotlin/Compose) 或 `LiveData` (Java/View) 向 UI **暴露（Expose）** 状态。
* 将可变的状态（`MutableStateFlow` / `MutableLiveData`）保持为 `private`，只在 `ViewModel` 内部修改。
* 在 `ViewModel` 内部封装所有业务逻辑（如 `rollDice()`）。

**示例 (Kotlin with StateFlow)**：

```kotlin
import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlin.random.Random

// 1. 定义 UI 状态的数据类
data class DiceUiState(
    val firstDieValue: Int? = null,
    val secondDieValue: Int? = null,
    val numberOfRolls: Int = 0,
)

// 2. 创建 ViewModel
class DiceRollViewModel : ViewModel() {

    // 私有的可变状态
    private val _uiState = MutableStateFlow(DiceUiState())

    // 暴露给 UI 的只读状态
    val uiState: StateFlow<DiceUiState> = _uiState.asStateFlow()

    // 3. 封装业务逻辑
    fun rollDice() {
        _uiState.update { currentState ->
            currentState.copy(
                firstDieValue = Random.nextInt(from = 1, until = 7),
                secondDieValue = Random.nextInt(from = 1, until = 7),
                numberOfRolls = currentState.numberOfRolls + 1,
            )
        }
    }
}
