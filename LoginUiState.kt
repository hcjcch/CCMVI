/**
 * 登录界面状态数据类
 */
data class LoginUiState(
    val username: String? = null,
    val password: String? = null,
    val isLoading: Boolean = false,
    val loginSuccess: Boolean = false,
    val errorMessage: String? = null
)