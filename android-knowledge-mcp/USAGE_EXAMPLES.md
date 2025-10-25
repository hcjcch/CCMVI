# Android知识库MCP服务使用示例

本文档提供了Android知识库MCP服务的详细使用示例，展示如何在JoyCode Agent中自动调用知识库获取架构指导。

## 🎯 核心使用场景

### 场景1: Android编码任务自动调用

当您给JoyCode Agent分配Android编码任务时，Agent会自动调用MCP服务获取相关规范：

```
用户: "帮我创建一个LoginViewModel"

JoyCode Agent自动执行:
1. 检测到Android编码任务
2. 自动调用 search_core_architecture 获取基础规范
3. 自动调用 search_component_guide 获取ViewModel指导
4. 基于获取的规范生成符合标准的代码
```

### 场景2: 手动工具调用

您也可以直接调用MCP工具获取特定信息：

## 📋 工具调用示例

### 1. 查询核心架构规范

```python
# 自动获取MVI架构和Kotlin编码规范
mcp_execute_tool("android-knowledge-rag", "search_core_architecture", {})
```

**返回内容包括:**
- MVI架构原则和分层设计
- Kotlin编码规范和命名约定
- 文件组织和项目结构规范

### 2. 查询组件使用指南

```python
# 查询ViewModel使用指南
mcp_execute_tool("android-knowledge-rag", "search_component_guide", {
    "component_type": "ViewModel",
    "query": "状态管理最佳实践"
})

# 查询Activity生命周期
mcp_execute_tool("android-knowledge-rag", "search_component_guide", {
    "component_type": "Activity"
})

# 查询LiveData vs Flow对比
mcp_execute_tool("android-knowledge-rag", "search_component_guide", {
    "component_type": "LiveData",
    "query": "与Flow的区别和选择"
})
```

**支持的组件类型:**
- `ViewModel` - ViewModel使用指南
- `Activity` - Activity生命周期和最佳实践
- `LiveData` - LiveData数据绑定
- `KotlinFlow` - Flow异步编程
- `UI` - Compose UI开发规范

### 3. 通用知识搜索

```python
# 搜索MVI架构相关知识
mcp_execute_tool("android-knowledge-rag", "search_knowledge", {
    "query": "MVI单向数据流",
    "top_k": 5,
    "filter_type": "core"
})

# 搜索组件相关最佳实践
mcp_execute_tool("android-knowledge-rag", "search_knowledge", {
    "query": "ViewModel LiveData 最佳实践",
    "top_k": 3,
    "filter_type": "components"
})

# 全局搜索
mcp_execute_tool("android-knowledge-rag", "search_knowledge", {
    "query": "Android Compose 状态管理",
    "top_k": 10,
    "filter_type": "all"
})
```

## 🔄 实际工作流程示例

### 示例1: 创建新的ViewModel

**用户请求:**
```
"帮我创建一个用户登录的ViewModel，包含用户名密码验证和登录状态管理"
```

**JoyCode Agent自动执行流程:**

1. **检测任务类型** → Android ViewModel编码任务
2. **自动调用核心架构查询:**
   ```python
   search_core_architecture()
   # 获取: MVI架构原则、Kotlin编码规范、文件命名规范
   ```

3. **自动调用组件指南查询:**
   ```python
   search_component_guide({
       "component_type": "ViewModel", 
       "query": "状态管理和数据验证"
   })
   # 获取: ViewModel最佳实践、StateFlow使用、业务逻辑封装
   ```

4. **生成符合规范的代码:**
   ```kotlin
   /**
    * 登录页面ViewModel
    * 负责管理登录状态和用户认证逻辑
    */
   class LoginViewModel : ViewModel() {
       // 遵循编码规范：私有可变状态
       private val _uiState = MutableStateFlow(LoginUiState())
       val uiState: StateFlow<LoginUiState> = _uiState.asStateFlow()
       
       // 遵循单一职责：专门处理登录逻辑
       fun login(username: String, password: String) {
           // 实现登录逻辑...
       }
   }
   ```

### 示例2: 架构设计咨询

**用户请求:**
```
"在MVI架构中，数据应该如何从Repository流向UI？"
```

**JoyCode Agent执行:**
```python
search_knowledge({
    "query": "MVI数据流 Repository UI",
    "top_k": 5,
    "filter_type": "core"
})
```

**返回架构指导:**
- 单向数据流原则
- Repository → ViewModel → UI 的数据传递
- 事件处理和状态更新机制

## 🎨 代码生成质量保证

通过MCP服务，JoyCode Agent生成的代码将自动遵循：

### ✅ 架构规范
- MVI单向数据流设计
- 清晰的分层结构
- 组件职责分离

### ✅ 编码规范  
- Kotlin编码标准
- 统一的命名约定
- 标准的注释格式

### ✅ 最佳实践
- 组件使用最佳实践
- 性能优化建议
- 安全性考虑

## 🔧 高级配置

### 自定义查询策略

您可以根据项目需要调整查询参数：

```python
# 精确搜索核心架构
search_knowledge({
    "query": "具体问题",
    "top_k": 3,           # 返回最相关的3个结果
    "filter_type": "core" # 只搜索核心架构文档
})

# 广泛搜索所有组件
search_knowledge({
    "query": "具体问题", 
    "top_k": 10,          # 返回更多结果
    "filter_type": "all"  # 搜索所有文档
})
```

### 组合查询策略

对于复杂需求，可以组合多个查询：

```python
# 1. 先获取核心架构
core_info = search_core_architecture()

# 2. 再获取特定组件指导  
component_info = search_component_guide({
    "component_type": "ViewModel"
})

# 3. 最后进行深度搜索
detailed_info = search_knowledge({
    "query": "ViewModel 状态管理 最佳实践",
    "top_k": 5
})
```

## 📊 效果对比

### 使用MCP服务前
```kotlin
// 可能不符合项目规范的代码
class LoginVM {
    var username = ""
    var password = ""
    
    fun doLogin() {
        // 直接处理逻辑...
    }
}
```

### 使用MCP服务后
```kotlin
/**
 * 登录ViewModel - 遵循MVI架构
 */
class LoginViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(LoginUiState())
    val uiState: StateFlow<LoginUiState> = _uiState.asStateFlow()
    
    /**
     * 处理用户登录
     */
    fun login(username: String, password: String) {
        _uiState.update { currentState ->
            currentState.copy(isLoading = true)
        }
        // 符合架构规范的实现...
    }
}
```

## 🎯 最佳实践建议

1. **信任自动调用**: 让JoyCode Agent自动调用MCP服务，无需手动干预
2. **具体描述需求**: 提供详细的功能描述，帮助Agent选择合适的查询策略  
3. **验证生成代码**: 检查生成的代码是否符合项目标准
4. **反馈改进**: 如发现不符合预期的结果，及时反馈以改进服务

---

通过Android知识库MCP服务，JoyCode Agent能够始终生成符合您项目标准的高质量Android代码！