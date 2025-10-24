import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

/**
 * 登录 ViewModel
 * 负责管理登录界面的状态和业务逻辑
 */
class LoginViewModel : ViewModel() {

    // 私有的可变状态
    private val _uiState = MutableStateFlow(LoginUiState())

    // 暴露给 UI 的只读状态
    val uiState: StateFlow<LoginUiState> = _uiState.asStateFlow()

    /**
     * 更新用户名
     */
    fun updateUsername(username: String) {
        _uiState.update { currentState ->
            currentState.copy(
                username = username,
                errorMessage = null
            )
        }
    }

    /**
     * 更新密码
     */
    fun updatePassword(password: String) {
        _uiState.update { currentState ->
            currentState.copy(
                password = password,
                errorMessage = null
            )
        }
    }

    /**
     * 执行登录操作
     */
    fun login() {
        val currentState = _uiState.value

        // 验证输入
        if (currentState.username.isNullOrBlank()) {
            _uiState.update { it.copy(errorMessage = "请输入用户名") }
            return
        }

        if (currentState.password.isNullOrBlank()) {
            _uiState.update { it.copy(errorMessage = "请输入密码") }
            return
        }

        // 设置加载状态
        _uiState.update { it.copy(isLoading = true, errorMessage = null) }

        // 模拟登录请求
        // 在实际项目中，这里应该调用网络请求
        simulateLoginRequest()
    }

    /**
     * 模拟登录请求
     */
    private fun simulateLoginRequest() {
        val currentState = _uiState.value

        // 简单的登录验证逻辑
        val isSuccess = currentState.username == "admin" && currentState.password == "123456"

        _uiState.update { currentState ->
            currentState.copy(
                isLoading = false,
                loginSuccess = isSuccess,
                errorMessage = if (!isSuccess) "用户名或密码错误" else null
            )
        }
    }

    /**
     * 重置登录状态
     */
    fun resetLoginState() {
        _uiState.update { LoginUiState() }
    }
}