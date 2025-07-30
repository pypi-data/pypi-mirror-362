#!/usr/bin/env python3
"""
PyPI 自动化发布脚本
用于构建和上传 agentrix 包到 PyPI，无需手动输入用户名和密码。
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

# 自动加载 .env 环境变量
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def run_command(cmd, check=True):
    print(f"运行命令: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"命令失败: {cmd}")
        print(f"错误输出: {result.stderr}")
        sys.exit(1)
    return result

def clean_build():
    print("清理构建文件...")
    build_dirs = ["build", "dist", "*.egg-info"]
    for pattern in build_dirs:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

def build_package():
    print("构建包...")
    run_command("uv build")

def upload_to_pypi(test=False):
    if test:
        token = os.environ.get("TESTPYPI_TOKEN")
        if not token:
            print("❌ 环境变量 TESTPYPI_TOKEN 未设置！")
            sys.exit(1)
        print("上传到 TestPyPI...")
        run_command(f"uv publish --publish-url https://test.pypi.org/legacy/ -u __token__ -p {token}")
    else:
        token = os.environ.get("PYPI_TOKEN")
        if not token:
            print("❌ 环境变量 PYPI_TOKEN 未设置！")
            sys.exit(1)
        print("上传到 PyPI...")
        run_command(f"uv publish -u __token__ -p {token}")

def main():
    print("开始 PyPI 发布流程...")
    if not Path("pyproject.toml").exists():
        print("错误: 请在项目根目录运行此脚本")
        sys.exit(1)
    clean_build()
    build_package()
    test_pypi = input("是否先上传到 TestPyPI 进行测试? (y/n): ").lower().strip()
    if test_pypi in ['y', 'yes']:
        upload_to_pypi(test=True)
        print("已上传到 TestPyPI")
        print("请检查: https://test.pypi.org/project/mcpmarket/")
        confirm = input("是否上传到正式 PyPI? (y/n): ").lower().strip()
        if confirm in ['y', 'yes']:
            upload_to_pypi(test=False)
            print("已上传到 PyPI")
            print("请检查: https://pypi.org/project/mcpmarket/")
        else:
            print("取消上传到正式 PyPI")
    else:
        confirm = input("确认上传到正式 PyPI? (y/n): ").lower().strip()
        if confirm in ['y', 'yes']:
            upload_to_pypi(test=False)
            print("已上传到 PyPI")
            print("请检查: https://pypi.org/project/mcpmarket/")
        else:
            print("取消上传")

if __name__ == "__main__":
    main() 