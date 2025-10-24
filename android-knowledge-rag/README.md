# Android知识库RAG检索系统

基于ChromaDB和SentenceTransformers的Android开发知识库智能检索系统。

## 功能特性

- 🔍 **智能语义搜索**: 基于向量相似度的语义检索
- 📊 **多粒度分块**: 支持文件级别、段落级别、句子级别的文档分块
- 🎯 **专业化内容**: 专门针对Android开发知识优化
- 🚀 **快速检索**: 毫秒级知识检索响应
- 🛠️ **易于扩展**: 支持添加更多文档和知识领域

## 安装和使用

### 1. 安装依赖

```bash
# 创建Python虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 构建知识库

```bash
# 使用默认文件级别粒度构建
./knowledge-search build

# 使用段落级别粒度构建
./knowledge-search build --granularity paragraph

# 使用句子级别粒度构建（更细粒度）
./knowledge-search build --granularity sentence

# 重置并重新构建
./knowledge-search build --reset
```

### 3. 检索知识

```bash
# 基本搜索
./knowledge-search "Activity生命周期"

# 返回更多结果
./knowledge-search "ViewModel状态管理" --top-k 10

# 按文件类型过滤
./knowledge-search "LiveData最佳实践" --file-type md

# 不同输出格式
./knowledge-search "Kotlin Flow" --format json
./knowledge-search "Compose UI" --format simple
```

### 4. 管理知识库

```bash
# 查看统计信息
./knowledge-search stats

# 重置数据库
./knowledge-search reset
```

## 命令行选项

### build - 构建知识库索引
- `--granularity, -g`: 文档分块粒度 (file/paragraph/sentence)
- `--reset`: 重置数据库

### search - 检索知识库
- `--top-k, -k`: 返回结果数量 (默认: 5)
- `--format`: 输出格式 (table/json/simple)
- `--file-type`: 按文件类型过滤 (md/txt/pdf)

### stats - 查看统计信息

### reset - 重置数据库

## 目录结构

```
android-knowledge-rag/
├── src/                    # 源代码
│   ├── config.py          # 配置文件
│   ├── document_processor.py  # 文档处理器
│   ├── vector_store.py    # 向量数据库
│   └── cli.py             # 命令行接口
├── data/                  # 数据目录
│   └── chroma_db/         # ChromaDB数据库
├── requirements.txt       # Python依赖
├── knowledge-search       # 主入口脚本
└── README.md             # 本文档
```

## 知识库结构

系统默认从 `../components/` 目录加载Android开发知识文档：

```
knowledge/
├── components/            # 知识库目录
│   ├── Activity.md       # Android Activity指南
│   ├── ViewModel.md      # ViewModel使用指南
│   ├── LiveData.md       # LiveData开发指南
│   ├── KotlinFlow.md     # Kotlin Flow完整指南
│   └── UI.md            # UI开发规范
└── android-knowledge-rag/ # RAG系统
```

## 技术架构

- **向量数据库**: ChromaDB - 本地向量存储和检索
- **嵌入模型**: all-MiniLM-L6-v2 - 轻量级多语言模型
- **文档处理**: 自定义文档分块器，支持多种粒度
- **CLI界面**: Click + Rich - 美观的命令行界面

## 配置说明

主要配置在 `src/config.py` 文件中：

```python
# 基础路径配置
KNOWLEDGE_DIR = BASE_DIR.parent / "components"  # 知识库目录
CHROMA_PATH = DATA_DIR / "chroma_db"           # 数据库路径

# 嵌入模型配置
EMBEDDING_MODEL = "all-MiniLM-L6-v2"           # 支持中文的轻量级模型

# 检索配置
DEFAULT_TOP_K = 5                               # 默认返回结果数
SIMILARITY_THRESHOLD = 0.7                      # 相似度阈值
```

## 性能优化建议

1. **分块粒度选择**:
   - `file`: 适合整体性强的文档，检索速度快
   - `paragraph`: 平衡精度和速度，推荐用于大多数场景
   - `sentence`: 最高精度，适合细粒度检索，但索引较大

2. **硬件要求**:
   - 最小内存: 2GB
   - 推荐内存: 4GB+
   - 存储: 根据文档数量，通常几百MB到几GB

## 故障排除

### 常见问题

1. **模块导入错误**
   ```bash
   export PYTHONPATH="${PYTHONPATH}:/path/to/android-knowledge-rag/src"
   ```

2. **嵌入模型下载失败**
   - 检查网络连接
   - 模型会自动下载到缓存目录

3. **数据库权限错误**
   ```bash
   chmod -R 755 data/
   ```

### 日志调试

使用详细模式查看调试信息：
```bash
./knowledge-search --verbose search "你的查询"
```

## 扩展开发

### 添加新的文档类型

1. 在 `document_processor.py` 中添加新的处理器
2. 在 `config.py` 的 `SUPPORTED_EXTENSIONS` 中添加文件扩展名

### 自定义嵌入模型

在 `config.py` 中修改 `EMBEDDING_MODEL`：
```python
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"  # 更强的多语言模型
```

### 集成到其他应用

```python
from src.vector_store import VectorStore
from src.document_processor import DocumentProcessor

# 初始化
vector_store = VectorStore()
results = vector_store.search("你的查询")
```

## License

MIT License