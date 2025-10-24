import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.flow.collectLatest

/**
 * 登录 Activity
 * 负责加载登录界面和处理页面跳转协议
 */
class LoginActivity : ComponentActivity() {

    // 使用 activity-ktx 的工具函数初始化 ViewModel
    private val viewModel: LoginViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            // 加载 LoginScreen
            LoginScreen(viewModel)
        }
    }
}

/**
 * 登录界面 Composable
 */
@Composable
fun LoginScreen(viewModel: LoginViewModel) {
    // 收集 UI 状态
    val uiState by viewModel.uiState.collectAsState()
    var showMessage by remember { mutableStateOf<String?>(null) }

    // 监听登录成功状态
    LaunchedEffect(uiState.loginSuccess) {
        if (uiState.loginSuccess) {
            showMessage = "登录成功！"
            // 这里可以跳转到主界面
        }
    }

    // 监听错误消息
    LaunchedEffect(uiState.errorMessage) {
        uiState.errorMessage?.let { message ->
            showMessage = message
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        // 标题
        Text(
            text = "登录",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.padding(bottom = 32.dp)
        )

        // 用户名输入框
        OutlinedTextField(
            value = uiState.username ?: "",
            onValueChange = { viewModel.updateUsername(it) },
            label = { Text("用户名") },
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            enabled = !uiState.isLoading
        )

        // 密码输入框
        OutlinedTextField(
            value = uiState.password ?: "",
            onValueChange = { viewModel.updatePassword(it) },
            label = { Text("密码") },
            visualTransformation = PasswordVisualTransformation(),
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 24.dp),
            enabled = !uiState.isLoading
        )

        // 登录按钮
        Button(
            onClick = { viewModel.login() },
            modifier = Modifier
                .fillMaxWidth()
                .height(48.dp),
            enabled = !uiState.isLoading
        ) {
            if (uiState.isLoading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(24.dp),
                    color = MaterialTheme.colorScheme.onPrimary
                )
            } else {
                Text("登录")
            }
        }

        // 重置按钮
        TextButton(
            onClick = { viewModel.resetLoginState() },
            modifier = Modifier.padding(top = 8.dp)
        ) {
            Text("重置")
        }

        // 显示消息
        showMessage?.let { message ->
            Spacer(modifier = Modifier.height(16.dp))
            Text(
                text = message,
                color = if (uiState.loginSuccess)
                    MaterialTheme.colorScheme.primary
                else
                    MaterialTheme.colorScheme.error,
                style = MaterialTheme.typography.bodyMedium
            )
        }

        // 提示信息
        Spacer(modifier = Modifier.height(24.dp))
        Text(
            text = "测试账号：admin / 123456",
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            style = MaterialTheme.typography.bodySmall
        )
    }
}