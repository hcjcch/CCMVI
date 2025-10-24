"""
命令行接口 - knowledge-search 命令
"""
import click
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich import print as rprint

from config import (
    KNOWLEDGE_DIR, DEFAULT_TOP_K,
    GRANULARITY_FILE, GRANULARITY_PARAGRAPH, GRANULARITY_SENTENCE,
    DEFAULT_GRANULARITY
)
from document_processor import DocumentProcessor
from vector_store import VectorStore

console = Console()

@click.group()
@click.version_option(version="1.0.0", prog_name="Android Knowledge RAG")
def cli():
    """
    Android开发知识库RAG检索系统

    用于快速检索Android开发相关知识的智能搜索引擎
    """
    pass

@cli.command()
@click.option('--granularity', '-g',
              type=click.Choice(['file', 'paragraph', 'sentence']),
              default=DEFAULT_GRANULARITY,
              help='文档分块粒度')
@click.option('--reset', is_flag=True, help='重置数据库')
def build(granularity, reset):
    """构建知识库索引"""
    console.print("[bold blue]🔨 开始构建Android知识库索引...[/bold blue]")

    try:
        # 检查知识库目录
        knowledge_path = KNOWLEDGE_DIR
        if not knowledge_path.exists():
            console.print(f"[red]❌ 知识库目录不存在: {knowledge_path}[/red]")
            return

        # 初始化文档处理器
        processor = DocumentProcessor(granularity=granularity)
        console.print(f"📝 使用粒度模式: [green]{granularity}[/green]")

        # 加载文档
        with console.status("[bold green]📚 加载知识库文档..."):
            documents = processor.load_documents(knowledge_path)

        if not documents:
            console.print("[yellow]⚠️  没有找到任何文档[/yellow]")
            return

        console.print(f"✅ 成功加载 [green]{len(documents)}[/green] 个文档片段")

        # 初始化向量数据库
        console.print("[bold blue]🗄️  初始化向量数据库...[/bold blue]")
        vector_store = VectorStore(reset_db=reset)

        # 添加文档到数据库
        with console.status("[bold green]📊 正在建立向量索引..."):
            vector_store.add_documents(documents)

        # 显示统计信息
        stats = vector_store.get_stats()
        console.print(Panel(
            f"[bold green]✅ 知识库构建完成！[/bold green]\n\n"
            f"📊 统计信息:\n"
            f"• 总文档数: {stats.get('total_documents', 0)}\n"
            f"• 分块粒度: {granularity}\n"
            f"• 嵌入模型: {stats.get('embedding_model', 'unknown')}\n"
            f"• 数据库路径: {stats.get('db_path', 'unknown')}",
            title="构建完成",
            border_style="green"
        ))

    except Exception as e:
        console.print(f"[red]❌ 构建失败: {e}[/red]")
        raise

@cli.command()
@click.argument('query')
@click.option('--top-k', '-k', default=DEFAULT_TOP_K, help='返回结果数量')
@click.option('--format', 'output_format',
              type=click.Choice(['table', 'json', 'simple']),
              default='table', help='输出格式')
@click.option('--file-type', type=click.Choice(['md', 'txt', 'pdf']),
              help='按文件类型过滤')
def search(query, top_k, output_format, file_type):
    """检索知识库"""
    console.print(f"[bold blue]🔍 搜索: '{query}'[/bold blue]")

    try:
        # 初始化向量数据库
        vector_store = VectorStore()

        # 构建过滤条件
        where_filter = None
        if file_type:
            where_filter = {"file_type": file_type}

        # 执行搜索
        with console.status("[bold green]🧠 正在搜索相关知识..."):
            results = vector_store.search(query, top_k=top_k, where=where_filter)

        if not results:
            console.print("[yellow]😔 没有找到相关知识[/yellow]")
            return

        # 根据格式输出结果
        if output_format == 'json':
            _print_results_json(results)
        elif output_format == 'simple':
            _print_results_simple(results)
        else:
            _print_results_table(query, results)

    except Exception as e:
        console.print(f"[red]❌ 搜索失败: {e}[/red]")

def _print_results_table(query, results):
    """以表格格式显示搜索结果"""
    table = Table(title=f"🔍 搜索结果: '{query}'", show_header=True, header_style="bold magenta")
    table.add_column("排名", style="cyan", width=6)
    table.add_column("文档", style="green", width=20)
    table.add_column("内容摘要", style="white", width=50)
    table.add_column("相似度", style="yellow", width=10)

    for i, result in enumerate(results, 1):
        content = result['content']
        metadata = result['metadata']

        # 截取内容作为摘要
        summary = content[:100] + "..." if len(content) > 100 else content

        # 获取相似度分数（如果有的话）
        similarity = f"{result.get('distance', 'N/A')}"

        # 文件名
        filename = metadata.get('filename', 'unknown')

        table.add_row(
            str(i),
            filename,
            summary,
            similarity
        )

    console.print(table)

    # 显示详细信息提示
    console.print(f"\n[dim]找到 {len(results)} 个相关结果。使用 --format simple 查看完整内容。[/dim]")

def _print_results_json(results):
    """以JSON格式显示搜索结果"""
    formatted_results = []
    for result in results:
        formatted_results.append({
            'id': result['id'],
            'content': result['content'],
            'metadata': result['metadata'],
            'similarity': result.get('distance')
        })

    console.print(json.dumps(formatted_results, ensure_ascii=False, indent=2))

def _print_results_simple(results):
    """以简单格式显示搜索结果"""
    for i, result in enumerate(results, 1):
        metadata = result['metadata']
        content = result['content']

        console.print(f"[bold cyan]--- 结果 {i} ---[/bold cyan]")
        console.print(f"[green]文件:[/green] {metadata.get('filename', 'unknown')}")
        console.print(f"[green]路径:[/green] {metadata.get('file_path', 'unknown')}")
        console.print(f"[green]类型:[/green] {metadata.get('chunk_type', 'unknown')}")

        # 显示内容
        console.print("\n[bold]内容:[/bold]")
        console.print(Panel(content, border_style="blue"))
        console.print()

@cli.command()
def stats():
    """显示知识库统计信息"""
    try:
        vector_store = VectorStore()
        stats = vector_store.get_stats()

        if not stats:
            console.print("[yellow]⚠️  无法获取统计信息，可能需要先构建知识库[/yellow]")
            return

        console.print(Panel(
            f"[bold]📊 知识库统计信息[/bold]\n\n"
            f"📁 总文档数: [green]{stats.get('total_documents', 0)}[/green]\n"
            f"🏷️  集合名称: {stats.get('collection_name', 'unknown')}\n"
            f"🤖 嵌入模型: {stats.get('embedding_model', 'unknown')}\n"
            f"💾 数据库路径: {stats.get('db_path', 'unknown')}",
            title="统计信息",
            border_style="blue"
        ))

    except Exception as e:
        console.print(f"[red]❌ 获取统计信息失败: {e}[/red]")

@cli.command()
@click.confirmation_option(prompt='确定要重置数据库吗？这将删除所有索引数据。')
def reset():
    """重置知识库数据库"""
    try:
        console.print("[bold red]🗑️  重置知识库数据库...[/bold red]")
        vector_store = VectorStore(reset_db=True)
        console.print("[green]✅ 数据库已重置[/green]")
        console.print("[dim]提示: 使用 'python cli.py build' 重新构建知识库[/dim]")
    except Exception as e:
        console.print(f"[red]❌ 重置失败: {e}[/red]")

if __name__ == '__main__':
    cli()