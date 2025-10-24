# Kotlin Flow AI 使用指南

## 核心概念

### Flow 基础
- **冷流**: 订阅时才开始发射数据
- **协程支持**: 基于协程，支持背压处理
- **结构化并发**: 与协程作用域绑定

```kotlin
// 基本操作
val flow = flow {
    repeat(3) {
        delay(1000)
        emit(it)
    }
}

// 转换和收集
flow.map { it * 2 }
    .filter { it > 0 }
    .collect { println(it) }
```

---

## StateFlow

### 核心特性
- **状态容器**: 总是有值，保存最新状态
- **自动去重**: 相同值不会重复发射
- **热流**: 无订阅者也保持状态

### 基础用法

```kotlin
class ViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(UiState.Idle)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    fun updateState(newState: UiState) {
        _uiState.value = newState
    }

    suspend fun loadData() {
        _uiState.value = UiState.Loading
        try {
            val data = repository.getData()
            _uiState.value = UiState.Success(data)
        } catch (e: Exception) {
            _uiState.value = UiState.Error(e.message)
        }
    }
}

// 观察状态
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect { state ->
            when (state) {
                is UiState.Loading -> showLoading()
                is UiState.Success -> showData(state.data)
                is UiState.Error -> showError(state.message)
            }
        }
    }
}
```

### 高级用法

```kotlin
// 合并多个状态
data class ProfileState(val name: String = "", val isLoading: Boolean = false)

val profileState: StateFlow<ProfileState> = combine(
    _name, _isLoading
) { name, isLoading ->
    ProfileState(name, isLoading)
}.stateIn(
    scope = viewModelScope,
    started = SharingStarted.WhileSubscribed(5000),
    initialValue = ProfileState()
)

// 状态转换
val userName: StateFlow<String> = userState
    .map { it.name }
    .stateIn(viewModelScope, SharingStarted.Eagerly, "")
```

---

## SharedFlow

### 核心特性
- **事件分发**: 热流，支持多订阅者
- **可配置缓冲**: 重放历史事件，控制背压
- **灵活配置**: 缓冲区大小和溢出策略

### 配置参数

```kotlin
val events = MutableSharedFlow<Event>(
    replay = 0,                           // 重放数量
    extraBufferCapacity = 1,              // 额外缓冲区
    onBufferOverflow = BufferOverflow.DROP_OLDEST  // 溢出策略
)

// 溢出策略
BufferOverflow.SUSPEND      // 挂起等待
BufferOverflow.DROP_OLDEST  // 丢弃最旧
BufferOverflow.DROP_LATEST   // 丢弃最新
```

### 基础用法

```kotlin
class EventManager {
    private val _events = MutableSharedFlow<Event>(
        replay = 0,
        extraBufferCapacity = 1,
        onBufferOverflow = BufferOverflow.DROP_OLDEST
    )

    val events: SharedFlow<Event> = _events.asSharedFlow()

    fun sendEvent(event: Event) {
        _events.tryEmit(event)  // 非挂起
    }

    suspend fun emitEvent(event: Event) {
        _events.emit(event)     // 挂起
    }
}

// 订阅事件
lifecycleScope.launch {
    eventManager.events
        .flowWithLifecycle(lifecycle, Lifecycle.State.STARTED)
        .collect { event ->
            handleEvent(event)
        }
}
```

---

## 使用场景对比

| 场景 | StateFlow | SharedFlow |
|------|----------|------------|
| UI状态管理 | ✅ 状态必须存在 | ❌ 状态可能为空 |
| 表单验证 | ✅ 需要当前状态 | ❌ 事件驱动 |
| 导航事件 | ❌ 状态会重放 | ✅ 单次事件 |
| 系统通知 | ❌ 状态持续 | ✅ 事件分发 |
| 数据缓存 | ✅ 状态容器 | ❌ 需要额外缓存 |

### 推荐配置

```kotlin
// UI状态
val uiState = MutableStateFlow(UiState())

// 单次事件
val events = MutableSharedFlow<Event>(
    replay = 0,
    extraBufferCapacity = 1
)

// 数据更新广播
val dataUpdates = MutableSharedFlow<DataUpdate>(
    replay = 1,
    extraBufferCapacity = 0
)
```

---

## 最佳实践

### ViewModel 架构

```kotlin
class UserViewModel(
    private val userRepository: UserRepository
) : ViewModel() {

    // UI状态 - StateFlow
    private val _uiState = MutableStateFlow(UserUiState())
    val uiState: StateFlow<UserUiState> = _uiState.asStateFlow()

    // 单次事件 - SharedFlow
    private val _events = MutableSharedFlow<UserEvent>(
        replay = 0,
        extraBufferCapacity = 1
    )
    val events: SharedFlow<UserEvent> = _events.asSharedFlow()

    private fun loadUsers() = viewModelScope.launch {
        _uiState.update { it.copy(isLoading = true) }

        userRepository.getUsers()
            .catch { error ->
                _uiState.update {
                    it.copy(isLoading = false, error = error.message)
                }
            }
            .collect { users ->
                _uiState.update {
                    it.copy(isLoading = false, users = users)
                }
            }
    }

    fun navigateToUser(userId: String) = viewModelScope.launch {
        _events.emit(UserEvent.NavigateToUser(userId))
    }
}
```

### 错误处理模式

```kotlin
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val exception: Throwable) : Result<Nothing>()
    object Loading : Result<Nothing>()
}

fun <T> safeFlow(apiCall: suspend () -> T): Flow<Result<T>> = flow {
    emit(Result.Loading)
    try {
        emit(Result.Success(apiCall()))
    } catch (e: Exception) {
        emit(Result.Error(e))
    }
}
```

---

## 常见陷阱避免

### StateFlow 陷阱

```kotlin
// ❌ 非原子操作
fun increment() {
    _count.value = _count.value + 1
}

// ✅ 原子操作
fun increment() {
    _count.update { it + 1 }
}

// ❌ 不必要的更新
fun updateName(name: String) {
    _uiState.value = _uiState.value.copy(name = name)
}

// ✅ 避免重复更新
fun updateName(name: String) {
    if (_uiState.value.name != name) {
        _uiState.value = _uiState.value.copy(name = name)
    }
}
```

### SharedFlow 陷阱

```kotlin
// ❌ 缓冲区过大
val events = MutableSharedFlow<Event>(replay = 100)

// ✅ 合理配置
val events = MutableSharedFlow<Event>(
    replay = 0,
    extraBufferCapacity = 10,
    onBufferOverflow = BufferOverflow.DROP_OLDEST
)

// ❌ 丢失事件
fun sendMassiveEvents() {
    repeat(10000) {
        _events.tryEmit(Event(it))  // 可能丢失
    }
}

// ✅ 正确处理背压
suspend fun sendEvents(events: List<Event>) {
    events.forEach { event ->
        _events.emit(event)  // 等待发送
    }
}
```

### 生命周期管理

```kotlin
// ✅ 正确的生命周期感知
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect { state ->
            updateUI(state)
        }
    }
}

// ✅ 或者使用 flowWithLifecycle
lifecycleScope.launch {
    viewModel.events
        .flowWithLifecycle(lifecycle, Lifecycle.State.STARTED)
        .collect { event ->
            handleEvent(event)
        }
}
```

---

## AI 使用规则总结

### 选择原则
- **StateFlow**: 需要状态、必须有值、UI状态管理
- **SharedFlow**: 事件驱动、一次性通知、多订阅者

### 实现要点
- 使用 `asStateFlow()` 和 `asSharedFlow()` 暴露不可变接口
- 正确配置缓冲区和溢出策略
- 使用 `repeatOnLifecycle` 或 `flowWithLifecycle` 处理生命周期
- 优先使用 `update` 函数进行原子状态更新
- 避免不必要的状态更新和内存泄漏

### 性能优化
- StateFlow 自动去重相同值
- 合理配置 SharedFlow 缓冲区大小
- 使用 `distinctUntilChanged` 过滤重复数据
- 及时取消协程避免内存泄漏