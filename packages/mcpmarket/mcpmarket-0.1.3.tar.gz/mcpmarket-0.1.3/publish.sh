#!/bin/bash

# 自动加载 .env 环境变量
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# PyPI 自动化发布脚本
set -e

echo "🚀 开始 PyPI 发布流程..."

# 检查是否在正确的目录
if [ ! -f "pyproject.toml" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 清理旧的构建文件
echo "🧹 清理构建文件..."
rm -rf build/ dist/ *.egg-info/

# 构建包
echo "📦 构建包..."
uv build

echo "✅ 构建成功！"

# 显示构建的文件
echo "📁 构建的文件:"
ls -la dist/

# 询问是否上传到 TestPyPI
read -p "是否先上传到 TestPyPI 进行测试? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -z "$TESTPYPI_TOKEN" ]; then
        echo "❌ 环境变量 TESTPYPI_TOKEN 未设置！"
        exit 1
    fi
    echo "📤 上传到 TestPyPI..."
    uv publish --publish-url https://test.pypi.org/legacy/ -u __token__ -p "$TESTPYPI_TOKEN"
    if [ $? -eq 0 ]; then
        echo "✅ 已上传到 TestPyPI"
        echo "🔍 请检查: https://test.pypi.org/project/mcpmarket/"
        read -p "是否上传到正式 PyPI? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if [ -z "$PYPI_TOKEN" ]; then
                echo "❌ 环境变量 PYPI_TOKEN 未设置！"
                exit 1
            fi
            echo "📤 上传到正式 PyPI..."
            uv publish -u __token__ -p "$PYPI_TOKEN"
            if [ $? -eq 0 ]; then
                echo "✅ 已上传到 PyPI"
                echo "🔍 请检查: https://pypi.org/project/mcpmarket/"
            else
                echo "❌ 上传到 PyPI 失败"
                exit 1
            fi
        else
            echo "⏭️  跳过上传到正式 PyPI"
        fi
    else
        echo "❌ 上传到 TestPyPI 失败"
        exit 1
    fi
else
    # 直接上传到正式 PyPI
    read -p "确认上传到正式 PyPI? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ -z "$PYPI_TOKEN" ]; then
            echo "❌ 环境变量 PYPI_TOKEN 未设置！"
            exit 1
        fi
        echo "📤 上传到正式 PyPI..."
        uv publish -u __token__ -p "$PYPI_TOKEN"
        if [ $? -eq 0 ]; then
            echo "✅ 已上传到 PyPI"
            echo "🔍 请检查: https://pypi.org/project/mcpmarket/"
        else
            echo "❌ 上传失败"
            exit 1
        fi
    else
        echo "⏭️  取消上传"
    fi
fi

echo "🎉 发布流程完成！" 