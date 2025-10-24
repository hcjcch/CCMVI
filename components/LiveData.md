# LiveData AI Coding 参考指南

## 核心概念
LiveData是Android Architecture Components中具有生命周期感知能力的可观察数据持有者类，只在组件活跃时通知观察者更新UI。

## 快速开始

### 依赖配置
```gradle
def lifecycle_version = "2.6.2"
implementation "androidx.lifecycle:lifecycle-livedata-ktx:$lifecycle_version"
implementation "androidx.lifecycle:lifecycle-viewmodel-ktx:$lifecycle_version"
```

### 基本使用模式

#### 1. ViewModel中创建LiveData
```kotlin
class UserViewModel : ViewModel() {
    private val _userData = MutableLiveData<User>()
    val userData: LiveData<User> = _userData
    
    fun updateUser(user: User) {
        _userData.value = user        // 主线程
        // _userData.postValue(user)  // 任意线程
    }
}
```

#### 2. Activity/Fragment中观察
```kotlin
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val viewModel = ViewModelProvider(this)[UserViewModel::class.java]
        viewModel.userData.observe(this) { user ->
            // 更新UI
        }
    }
}
```

## 核心API

### LiveData类型
- **MutableLiveData**: 可修改的LiveData
- **MediatorLiveData**: 合并多个LiveData源

### 数据更新
- **setValue()**: 主线程更新
- **postValue()**: 任意线程更新

### 数据转换
```kotlin
// map转换
val userName = userData.map { it.name }

// switchMap转换
val userPosts = userId.switchMap { id ->
    repository.getPostsByUserId(id)
}
```

## 最佳实践

### 1. 数据封装
```kotlin
// ✅ 推荐
class ViewModel {
    private val _data = MutableLiveData<String>()
    val data: LiveData<String> = _data
}

// ❌ 不推荐
class ViewModel {
    val data = MutableLiveData<String>()  // 外部可修改
}
```

### 2. 生命周期安全
```kotlin
// ✅ 正确
viewModel.data.observe(this) { data -> updateUI(data) }

// ❌ 错误 - 可能内存泄漏
viewModel.data.observeForever { data -> updateUI(data) }
```

### 3. 线程安全
```kotlin
class ViewModel : ViewModel() {
    private val _data = MutableLiveData<String>()
    
    fun updateFromBackground() {
        viewModelScope.launch {
            val result = withContext(Dispatchers.IO) { fetchData() }
            _data.value = result  // 主线程更新
        }
    }
}
```

## 常见场景

### 自定义LiveData
```kotlin
class LocationLiveData(context: Context) : LiveData<Location>() {
    override fun onActive() {
        // 开始位置监听
    }
    
    override fun onInactive() {
        // 停止位置监听
    }
}
```

### 与协程结合
```kotlin
fun fetchData(): LiveData<Result<User>> = liveData {
    emit(Result.Loading)
    try {
        val user = api.getUser()
        emit(Result.Success(user))
    } catch (e: Exception) {
        emit(Result.Error(e))
    }
}
```

### Room集成
```kotlin
@Dao
interface UserDao {
    @Query("SELECT * FROM users")
    fun getAllUsers(): LiveData<List<User>>  // 自动返回LiveData
}
```

## 常见错误

### 1. 内存泄漏
- 使用`observe(this)`而不是`observeForever()`
- 避免在ViewModel中持有Context引用

### 2. 线程问题
- 主线程使用`setValue()`
- 后台线程使用`postValue()`

### 3. 数据重复通知
```kotlin
val data = _data.distinctUntilChanged()  // 避免重复通知
```

## 测试
```kotlin
@ExtendWith(InstantTaskExecutorExtension::class)
class ViewModelTest {
    @Test
    fun testDataUpdate() {
        val viewModel = UserViewModel()
        val observer = mockk<Observer<User>>(relaxed = true)
        
        viewModel.userData.observeForever(observer)
        viewModel.updateUser(testUser)
        
        verify { observer.onChanged(testUser) }
    }
}
```

## 关键要点
- 生命周期感知，自动管理观察者
- 配置更改时数据保持
- 只在活跃状态时通知UI更新
- 避免内存泄漏
- 线程安全的数据更新