#!/bin/bash

# PyPI 自动化发布脚本
set -e

# 从 .pypirc 文件加载认证信息
if [ -f ".pypirc" ]; then
    export UV_PUBLISH_USERNAME=__token__
    export UV_PUBLISH_PASSWORD=$(grep "password" .pypirc | head -1 | cut -d'=' -f2 | xargs)
    export UV_PUBLISH_TEST_PASSWORD=$(grep "password" .pypirc | tail -1 | cut -d'=' -f2 | xargs)
    echo "✅ 从 .pypirc 文件加载认证信息"
elif [ -f "$HOME/.pypirc" ]; then
    export UV_PUBLISH_USERNAME=__token__
    export UV_PUBLISH_PASSWORD=$(grep "password" "$HOME/.pypirc" | head -1 | cut -d'=' -f2 | xargs)
    export UV_PUBLISH_TEST_PASSWORD=$(grep "password" "$HOME/.pypirc" | tail -1 | cut -d'=' -f2 | xargs)
    echo "✅ 从 ~/.pypirc 文件加载认证信息"
else
    echo "⚠️  警告: 未找到 .pypirc 文件，将需要手动输入认证信息"
fi

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
    echo "📤 上传到 TestPyPI..."
    uv publish --publish-url https://test.pypi.org/legacy/
    if [ $? -eq 0 ]; then
        echo "✅ 已上传到 TestPyPI"
        echo "🔍 请检查: https://test.pypi.org/project/mcpmarket/"
        read -p "是否上传到正式 PyPI? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "📤 上传到正式 PyPI..."
            uv publish
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
        echo "📤 上传到正式 PyPI..."
        uv publish
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