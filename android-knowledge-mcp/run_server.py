#!/usr/bin/env python3
"""
Android知识库MCP服务器启动脚本
"""

import os
import sys
from pathlib import Path

def main():
    """启动MCP服务器"""
    # 获取项目根目录
    project_root = Path(__file__).parent
    
    # 激活虚拟环境（如果存在）
    venv_python = project_root / "venv" / "bin" / "python"
    if venv_python.exists():
        # 使用虚拟环境的Python
        os.execv(str(venv_python), [str(venv_python), str(project_root / "src" / "mcp_server.py")])
    else:
        # 使用系统Python
        os.execv(sys.executable, [sys.executable, str(project_root / "src" / "mcp_server.py")])

if __name__ == "__main__":
    main()