#!/usr/bin/env python3
"""
调试入口文件 - 用于在 IDE 中调试 Agentrix

使用方法：
1. 在 IDE 中打开此文件
2. 修改下面的 sys.argv 来模拟命令行参数
3. 设置断点
4. 运行调试

示例：
- 调试 list 命令：sys.argv = ['debug_agentrix.py', 'list']
- 调试 search 命令：sys.argv = ['debug_agentrix.py', 'search', 'weather']
- 调试 install 命令：sys.argv = ['debug_agentrix.py', 'install', '@turkyden/weather', '--client', 'cursor']
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

# 设置工作目录
os.chdir(project_root)

# 模拟命令行参数（修改这里来调试不同命令）
sys.argv = [
    'debug_agentrix.py',  # 脚本名
    'list',              # 命令
    # 'clients'          # 参数（如果需要）
]

# 导入并运行主程序
if __name__ == "__main__":
    from agentrix.cli import main_cli
    
    print(f"🐛 调试模式：{' '.join(sys.argv[1:])}")
    print(f"📁 工作目录：{os.getcwd()}")
    print(f"🐍 Python 路径：{sys.path[:3]}...")
    print("-" * 50)
    
    # 运行主程序
    main_cli() 