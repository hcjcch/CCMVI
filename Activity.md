# AI 编程指南：Android Activity

## 如何使用 Activity

**职责**：
- 处理页面跳转协议
- 初始化 ViewModel
- 加载对应的 Entry Screen

**原则**：
- 仅作为界面载体，不包含业务逻辑
- 一个 Activity 对应一个 Entry Screen（特殊情况使用 NavController）
- 初始化 ViewModel 时，使用 activity-ktx 的工具函数：by viewModels

## 一些例子

```kotlin
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            // 加载 Composeable 标记的 Screen
        }
    }
}
```