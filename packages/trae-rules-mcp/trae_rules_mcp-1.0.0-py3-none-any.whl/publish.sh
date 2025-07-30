#!/bin/bash

# 🚀 Trae Rules MCP 发布脚本
# 用于自动化发布流程

set -e  # 遇到错误立即退出

echo "🚀 开始 Trae Rules MCP 发布流程..."

# 检查是否在正确的目录
if [ ! -f "pyproject.toml" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 获取当前版本
VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
echo "📦 当前版本: $VERSION"

# 确认发布
read -p "🤔 确认发布版本 $VERSION 吗? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 发布已取消"
    exit 1
fi

echo "🧹 清理旧的构建文件..."
rm -rf dist/ build/ *.egg-info/

echo "🔨 构建分发包..."
uv run python -m build

echo "✅ 检查分发包..."
uv run twine check dist/*

echo "📋 分发包内容:"
ls -la dist/

echo ""
echo "🎯 发布选项:"
echo "1. 发布到 TestPyPI (推荐先测试)"
echo "2. 发布到正式 PyPI"
echo "3. 仅构建，不发布"
read -p "请选择 (1/2/3): " -n 1 -r
echo

case $REPLY in
    1)
        echo "🧪 发布到 TestPyPI..."
        uv run twine upload --repository testpypi dist/*
        echo "✅ 已发布到 TestPyPI!"
        echo "🔗 查看: https://test.pypi.org/project/trae-rules-mcp/"
        echo "📦 测试安装: pip install --index-url https://test.pypi.org/simple/ trae-rules-mcp"
        ;;
    2)
        echo "🚀 发布到正式 PyPI..."
        read -p "⚠️  确认发布到正式 PyPI? 这个操作不可撤销! (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            uv run twine upload dist/*
            echo "🎉 已发布到 PyPI!"
            echo "🔗 查看: https://pypi.org/project/trae-rules-mcp/"
            echo "📦 安装: pip install trae-rules-mcp"
            
            # 创建 Git 标签
            echo "🏷️  创建 Git 标签..."
            git tag -a "v$VERSION" -m "Release version $VERSION"
            echo "📤 推送标签到远程仓库..."
            git push origin "v$VERSION"
            echo "✅ Git 标签已创建并推送"
        else
            echo "❌ 发布已取消"
        fi
        ;;
    3)
        echo "✅ 构建完成，未发布"
        echo "📁 分发包位于 dist/ 目录"
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "🎯 下一步建议:"
echo "1. 更新 CHANGELOG.md"
echo "2. 在 GitHub 上创建 Release"
echo "3. 通知用户新版本发布"
echo "4. 监控下载统计和用户反馈"

echo "✨ 发布流程完成!"